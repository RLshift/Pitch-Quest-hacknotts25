"""
Dependencies:
    pip install sounddevice numpy
"""

import math
import queue
import threading
import time
import numpy as np
import sounddevice as sd
from collections import deque

# ---------- SETTINGS ----------
SAMPLE_RATE = 44100
FRAME_SIZE = 4096
HOP_SIZE = 512
SMOOTHING = 6
BUFFER_MAX_SECONDS = 5.0
MIN_FREQUENCY = 250.0
MAX_FREQUENCY = 2000.0
LOWEST_NOTE_HZ = 246.0
NOISE_MULTIPLIER = 1.8
ENERGY_HISTORY = deque(maxlen=50)
NOTE_NAMES = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

device = None

# Internal queues
_audio_data_queue = queue.Queue(maxsize=int(SAMPLE_RATE / HOP_SIZE * BUFFER_MAX_SECONDS))
_note_queue = queue.Queue(maxsize=100)

_stop_flag = threading.Event()
_latest_note = None


# ---------- utils ----------
def freq_to_note_name(freq, A4=440.0):
    midi = 69 + 12 * math.log2(freq / A4)
    midi_round = int(round(midi))
    note_name = NOTE_NAMES[midi_round % 12]
    octave = (midi_round // 12) - 1
    return f"{note_name}{octave}"

def detect_pitch_autocorr(x, fs, fmin=MIN_FREQUENCY, fmax=MAX_FREQUENCY):
    x = x * np.hanning(len(x))
    n = len(x)
    size = 1 << int(np.ceil(np.log2(2 * n)))
    X = np.fft.rfft(x, n=size)
    acf = np.fft.irfft(np.abs(X)**2, n=size)[:n]
    acf /= np.max(np.abs(acf)) + 1e-8

    lag_min = int(round(fs / fmax))
    lag_max = int(round(fs / fmin))
    if lag_max >= len(acf): lag_max = len(acf)-1
    lag_min = max(lag_min, 2)
    window = acf[lag_min:lag_max+1]
    if len(window) == 0: return None

    peak_idx = np.argmax(window) + lag_min
    peak_value = acf[peak_idx]
    if peak_value < 0.3: return None

    return fs / peak_idx


# ---------- main logic ----------
def _audio_callback(indata, frames, time_info, status):
    if status: print(status)
    try:
        _audio_data_queue.put_nowait(indata[:,0].copy())
    except queue.Full:
        pass


def _audio_loop():
    global _latest_note
    stream = sd.InputStream(channels=1, samplerate=SAMPLE_RATE, blocksize=HOP_SIZE,
                            callback=_audio_callback, device=device)

    buffer = np.zeros(0, dtype=np.float32)
    recent_freqs = []
    last_note, note_start = None, None

    with stream:
        while not _stop_flag.is_set():
            try:
                data = _audio_data_queue.get(timeout=0.05)
            except queue.Empty:
                continue

            buffer = np.concatenate((buffer, data))
            while len(buffer) >= FRAME_SIZE:
                frame = buffer[:FRAME_SIZE]
                buffer = buffer[HOP_SIZE:]
                frame = frame.astype(np.float32)

                energy = np.mean(frame**2)
                ENERGY_HISTORY.append(energy)
                threshold = np.mean(ENERGY_HISTORY)*NOISE_MULTIPLIER
                if energy < threshold: continue

                freq = detect_pitch_autocorr(frame, SAMPLE_RATE)
                if not freq or freq < LOWEST_NOTE_HZ: continue

                recent_freqs.append(freq)
                if len(recent_freqs) > SMOOTHING: recent_freqs.pop(0)
                freq = np.median(recent_freqs)
                note = freq_to_note_name(freq)
                _latest_note = note

                current_time = time.time()
                if note != last_note:
                    if last_note and note_start:
                        duration = current_time - note_start
                        _note_queue.put_nowait({
                            "note": last_note,
                            "duration": duration,
                            "timestamp": current_time
                        })
                    last_note, note_start = note, current_time

            time.sleep(0.001)


# ---------- Public commands ----------
def start_listening():
    _stop_flag.clear()
    t = threading.Thread(target=_audio_loop, daemon=True)
    t.start()

def get_latest_note():
    return _latest_note

def get_note_event(block=False, timeout=None):
    try:
        return _note_queue.get(block=block, timeout=timeout)
    except queue.Empty:
        return None

def stop_listening():
    _stop_flag.set()


# ---------- Standalone test ----------
if __name__ == "__main__":
    print("Listening... Press Ctrl+C to stop.")
    start_listening()
    try:
        while True:
            event = get_note_event(timeout=1)
            if event:
                print(f"{event['note']} ({event['duration']:.2f}s)")
    except KeyboardInterrupt:
        stop_listening()
        print("Stopped.")