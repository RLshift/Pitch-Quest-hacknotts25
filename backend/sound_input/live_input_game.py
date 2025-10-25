# Dependencies:
# pip install sounddevice numpy

import queue
import sys
import math
import time
import numpy as np
import sounddevice as sd
from collections import deque
import random

# ---------- Adaptive noise cancellation ----------
ENERGY_HISTORY = deque(maxlen=50)
NOISE_MULTIPLIER = 1.8

# ---------- SETTINGS ----------
SAMPLE_RATE = 44100
FRAME_SIZE = 4096
HOP_SIZE = 512
BUFFER_MAX_SECONDS = 5.0
SMOOTHING = 6

# ---------- Note range ----------
MIN_FREQUENCY = 250.0
MAX_FREQUENCY = 2000.0
LOWEST_NOTE_HZ = 246.0

device = None

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']

# ---------- frequency ↔ note conversion ----------
def freq_to_note_name(freq, A4=440.0):
    if freq is None or freq <= 0:
        return ("-", None, None)
    midi = 69 + 12 * math.log2(freq / A4)
    midi_round = int(round(midi))
    note_name = NOTE_NAMES[midi_round % 12]
    octave = (midi_round // 12) - 1
    cents = int(round((midi - midi_round) * 100))
    return (f"{note_name}{octave}", midi_round, cents)

def midi_to_freq(midi):
    return 440.0 * (2 ** ((midi - 69) / 12))

# ---------- pitch detection ----------
def detect_pitch_autocorr(x, fs, fmin=MIN_FREQUENCY, fmax=MAX_FREQUENCY):
    x = x * np.hanning(len(x))
    n = len(x)
    size = 1 << (int(np.ceil(np.log2(2 * n))))
    X = np.fft.rfft(x, n=size)
    S = np.abs(X)**2
    acf = np.fft.irfft(S, n=size)
    acf = acf[:n]
    acf /= np.max(np.abs(acf)) + 1e-8

    lag_min = int(round(fs / fmax))
    lag_max = int(round(fs / fmin))
    if lag_max >= len(acf):
        lag_max = len(acf) - 1
    if lag_min < 2:
        lag_min = 2

    window = acf[lag_min:lag_max+1]
    if len(window) == 0:
        return None

    peak_idx = np.argmax(window) + lag_min
    peak_value = acf[peak_idx]
    if peak_value < 0.3:
        return None

    if 1 <= peak_idx < len(acf) - 1:
        alpha = acf[peak_idx - 1]
        beta = acf[peak_idx]
        gamma = acf[peak_idx + 1]
        p = 0.5 * (alpha - gamma) / (alpha - 2*beta + gamma)
        peak_lag = peak_idx + p
    else:
        peak_lag = float(peak_idx)

    if peak_lag <= 0:
        return None

    freq = fs / peak_lag
    if not (fmin * 0.9 <= freq <= fmax * 1.1):
        return None

    return freq

# ---------- Audio callback ----------
q = queue.Queue(maxsize=int(SAMPLE_RATE / HOP_SIZE * BUFFER_MAX_SECONDS))

def audio_callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    data = indata[:, 0] if indata.ndim > 1 else indata
    try:
        q.put_nowait(data.copy())
    except queue.Full:
        pass

# ---------- Pick random target note ----------
def pick_random_note():
    # Limit to musical range (C4–B5)
    midi = random.randint(60, 83)  # 60 = C4, 83 = B5
    note_name = NOTE_NAMES[midi % 12] + str((midi // 12) - 1)
    freq = midi_to_freq(midi)
    print(f"\n🎯 Play this note: {note_name} ({freq:.1f} Hz)")
    return note_name, midi, freq

# ---------- Main loop ----------
def run_realtime():
    stream = sd.InputStream(
        channels=1, samplerate=SAMPLE_RATE, blocksize=HOP_SIZE,
        callback=audio_callback, device=device
    )

    with stream:
        print("🎵 Starting note training game...")
        target_note, target_midi, target_freq = pick_random_note()
        buffer = np.zeros(0, dtype=np.float32)
        recent_freqs = []

        try:
            while True:
                data = q.get()
                buffer = np.concatenate((buffer, data))

                while len(buffer) >= FRAME_SIZE:
                    frame = buffer[:FRAME_SIZE]
                    buffer = buffer[HOP_SIZE:]

                    frame = frame.astype(np.float32)
                    energy = np.sum(frame ** 2) / len(frame)
                    ENERGY_HISTORY.append(energy)
                    adaptive_threshold = np.mean(
                        ENERGY_HISTORY) * NOISE_MULTIPLIER if ENERGY_HISTORY else 1e-6

                    if energy < adaptive_threshold:
                        continue

                    freq = detect_pitch_autocorr(frame, SAMPLE_RATE)
                    if freq is None or freq < LOWEST_NOTE_HZ:
                        continue

                    recent_freqs.append(freq)
                    if len(recent_freqs) > SMOOTHING:
                        recent_freqs.pop(0)
                    display_freq = float(np.median(recent_freqs))

                    note_name, midi, cents = freq_to_note_name(display_freq)
                    if note_name == "-":
                        continue

                    # Check if it matches the target
                    if abs(display_freq - target_freq) < 15:  # Hz tolerance
                        print(f"✅ Well done!! You played {note_name} ({display_freq:.1f} Hz)")
                        time.sleep(1.5)
                        target_note, target_midi, target_freq = pick_random_note()
                        recent_freqs.clear()

                time.sleep(0.001)

        except KeyboardInterrupt:
            print("\n🎵 Game stopped by user.")
        except Exception as e:
            print("\nError:", e)
        finally:
            stream.close()

if __name__ == "__main__":
    run_realtime()
