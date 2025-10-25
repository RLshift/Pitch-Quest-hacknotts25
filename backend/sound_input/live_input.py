"""
# Dependencies:
pip install sounddevice numpy
"""

import queue
import sys
import math
import time
import numpy as np
import sounddevice as sd
from collections import deque

# ---------- Adaptive noise cancellation ----------
ENERGY_HISTORY = deque(maxlen=50)  # store past energies
NOISE_MULTIPLIER = 1.8  # lower = more sensitive, higher = more strict

# ---------- SETTINGS ----------
SAMPLE_RATE = 44100        # Hz
FRAME_SIZE = 4096          # bigger = better low-frequency detection
HOP_SIZE = 512             # how often we run detection (in samples)
BUFFER_MAX_SECONDS = 5.0   # safety cap for internal queue
SMOOTHING = 6              # number of recent frequency estimates to median-smooth

# Limits for expected pitch (helps avoid octave errors)
MIN_FREQUENCY = 250.0     # e.g., low C2 ~ 65Hz
MAX_FREQUENCY = 2000.0   # upper bound for detection
LOWEST_NOTE_HZ = 246.0   # B3 lower

device = None

# ---------- frequency -> note ----------
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F',
              'F#', 'G', 'G#', 'A', 'A#', 'B']


def freq_to_note_name(freq, A4=440.0):
    if freq is None or freq <= 0:
        return ("-", None, None)
    midi = 69 + 12 * math.log2(freq / A4)
    midi_round = int(round(midi))
    note_name = NOTE_NAMES[midi_round % 12]
    octave = (midi_round // 12) - 1
    cents = int(round((midi - midi_round) * 100))
    return (f"{note_name}{octave}", midi_round, cents)


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


# ---------- audio callback ----------
q = queue.Queue(maxsize=int(SAMPLE_RATE / HOP_SIZE * BUFFER_MAX_SECONDS))


def audio_callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    if indata.ndim > 1:
        data = indata[:, 0]
    else:
        data = indata
    try:
        q.put_nowait(data.copy())
    except queue.Full:
        pass


def run_realtime():
    stream = sd.InputStream(
        channels=1, samplerate=SAMPLE_RATE, blocksize=HOP_SIZE,
        callback=audio_callback, device=device
    )

    with stream:
        print("Listening: Play a note!")
        buffer = np.zeros(0, dtype=np.float32)
        recent_freqs = []
        last_note = None
        note_start_time = None

        try:
            while True:
                data = q.get()
                buffer = np.concatenate((buffer, data))

                while len(buffer) >= FRAME_SIZE:
                    frame = buffer[:FRAME_SIZE]
                    buffer = buffer[HOP_SIZE:]

                    if frame.dtype.kind in 'iu':
                        frame = frame.astype(np.float32) / np.iinfo(frame.dtype).max
                    else:
                        frame = frame.astype(np.float32)

                    energy = np.sum(frame ** 2) / len(frame)
                    ENERGY_HISTORY.append(energy)
                    adaptive_threshold = np.mean(
                        ENERGY_HISTORY) * NOISE_MULTIPLIER if ENERGY_HISTORY else 1e-6

                    if energy < adaptive_threshold:
                        freq = None
                    else:
                        freq = detect_pitch_autocorr(frame, SAMPLE_RATE)

                    display_freq = None
                    if freq is not None and freq >= LOWEST_NOTE_HZ:
                        recent_freqs.append(freq)
                        if len(recent_freqs) > SMOOTHING:
                            recent_freqs.pop(0)
                        display_freq = float(np.median(recent_freqs))

                    if display_freq is not None:
                        note_name, midi, cents = freq_to_note_name(display_freq)

                        # Start timer if new note
                        if note_name != last_note:
                            if last_note is not None and note_start_time is not None:
                                duration = time.time() - note_start_time
                                print(f"→ {last_note} duration: {duration:.2f}s")

                            cent_str = f"{cents:+}¢" if cents is not None else ""
                            print(f"Freq: {display_freq:7.2f} Hz → {note_name} {cent_str}")
                            last_note = note_name
                            note_start_time = time.time()

                time.sleep(0.001)

        except KeyboardInterrupt:
            # Print duration of last note before exiting
            if last_note and note_start_time:
                duration = time.time() - note_start_time
                print(f"\n→ {last_note} duration: {duration:.2f}s")
            print("\nRecording stopped by user")
        except Exception as e:
            print("\nError:", e)
        finally:
            stream.close()


if __name__ == "__main__":
    run_realtime()