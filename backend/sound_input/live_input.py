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
import threading
from collections import deque

# ---------- Adaptive noise cancellation ----------
ENERGY_HISTORY = deque(maxlen=50)  # store past energies
NOISE_MULTIPLIER = 1.8  # lower = more sensitive, higher = more strict

# ---------- SETTINGS ----------
SAMPLE_RATE = 44100        # Hz
FRAME_SIZE = 4096          # bigger = better low-frequency detection
HOP_SIZE = 512             # how often we run detection (in samples)
SMOOTHING = 6              # number of recent frequency estimates to median-smooth
BUFFER_MAX_SECONDS = 5.0

# Limits for expected pitch (helps avoid octave errors)
MIN_FREQUENCY = 250.0
MAX_FREQUENCY = 2000.0
LOWEST_NOTE_HZ = 246.0  # B3 lower

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


# ---------- Thread-safe note queue ----------
note_queue = queue.Queue(maxsize=100)  # shared with your game
_audio_data_queue = queue.Queue(maxsize=int(SAMPLE_RATE / HOP_SIZE * BUFFER_MAX_SECONDS))
stop_flag = False


def audio_callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    data = indata[:, 0] if indata.ndim > 1 else indata
    try:
        _audio_data_queue.put_nowait(data.copy())
    except queue.Full:
        pass


def _audio_loop():
    global stop_flag

    stream = sd.InputStream(
        channels=1, samplerate=SAMPLE_RATE, blocksize=HOP_SIZE,
        callback=audio_callback, device=device
    )

    with stream:
        buffer = np.zeros(0, dtype=np.float32)
        recent_freqs = []
        last_note = None
        note_start_time = None

        while not stop_flag:
            try:
                data = _audio_data_queue.get(timeout=0.05)
            except queue.Empty:
                continue

            buffer = np.concatenate((buffer, data))

            while len(buffer) >= FRAME_SIZE:
                frame = buffer[:FRAME_SIZE]
                buffer = buffer[HOP_SIZE:]

                frame = frame.astype(np.float32)
                energy = np.sum(frame ** 2) / len(frame)
                ENERGY_HISTORY.append(energy)
                adaptive_threshold = np.mean(ENERGY_HISTORY) * NOISE_MULTIPLIER if ENERGY_HISTORY else 1e-6

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

                # Handle note start/duration tracking
                current_time = time.time()
                if note_name != last_note:
                    if last_note is not None and note_start_time is not None:
                        duration = current_time - note_start_time
                        # Send finished note to queue with duration
                        try:
                            note_queue.put_nowait({
                                "note": last_note,
                                "duration": duration,
                                "timestamp": current_time
                            })
                        except queue.Full:
                            note_queue.get_nowait()  # drop oldest
                            note_queue.put_nowait({
                                "note": last_note,
                                "duration": duration,
                                "timestamp": current_time
                            })
                    # Start new note
                    last_note = note_name
                    note_start_time = current_time


def start_audio_thread():
    thread = threading.Thread(target=_audio_loop, daemon=True)
    thread.start()
    return thread


def stop_audio():
    global stop_flag
    stop_flag = True

if __name__ == "__main__":
    print("Starting live audio input... (Press Ctrl+C to stop)")
    start_audio_thread()

    try:
        while True:
            # Continuously read detected notes from the queue
            try:
                note_event = note_queue.get(timeout=1.0)
                print(f"{note_event['note']}  ({note_event['duration']:.2f}s)")
            except queue.Empty:
                pass
    except KeyboardInterrupt:
        print("\nStopping...")
        stop_audio()
