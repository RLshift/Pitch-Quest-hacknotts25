# Dependencies:
# pip install librosa numpy soundfile

import math
import numpy as np
import librosa
import csv

# ---------- SETTINGS ----------
SAMPLE_RATE = 44100
FRAME_SIZE = 4096
HOP_SIZE = 512
SMOOTHING = 50
MIN_FREQUENCY = 250.0
MAX_FREQUENCY = 2000.0
LOWEST_NOTE_HZ = 246.0  # B3 lower
OUTPUT_CSV = "output/nights.csv"
MIN_NOTE_DURATION = 0.1  # ignore notes shorter than this (in seconds)

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


def analyze_mp3_to_csv(filename):
    print(f"Analyzing '{filename}'...")

    # Load audio
    y, sr = librosa.load(filename, sr=SAMPLE_RATE, mono=True)
    num_frames = (len(y) - FRAME_SIZE) // HOP_SIZE
    recent_freqs = []
    last_note = None
    note_start_time = None
    note_events = []

    # Process audio frame-by-frame
    for i in range(num_frames):
        start = i * HOP_SIZE
        frame = y[start:start + FRAME_SIZE]
        if len(frame) < FRAME_SIZE:
            break

        freq = detect_pitch_autocorr(frame, sr)
        display_freq = None
        if freq is not None and freq >= LOWEST_NOTE_HZ:
            recent_freqs.append(freq)
            if len(recent_freqs) > SMOOTHING:
                recent_freqs.pop(0)
            display_freq = float(np.median(recent_freqs))

        current_time = start / sr

        if display_freq is not None:
            note_name, midi_num, cents = freq_to_note_name(display_freq)
            if note_name != last_note:
                # Save previous note
                if last_note is not None and note_start_time is not None:
                    duration = current_time - note_start_time
                    if duration >= MIN_NOTE_DURATION:
                        note_events.append((last_note, midi_last, note_start_time, duration))
                        print(f"→ {last_note} duration: {duration:.2f}s")
                last_note = note_name
                midi_last = midi_num
                note_start_time = current_time

    # Final note
    if last_note and note_start_time:
        duration = (len(y) / sr) - note_start_time
        if duration >= MIN_NOTE_DURATION:
            note_events.append((last_note, midi_last, note_start_time, duration))
            print(f"→ {last_note} duration: {duration:.2f}s")

    # Export CSV
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["note_name", "midi_number", "start_time_sec", "duration_sec"])
        writer.writerows(note_events)

    print(f"\n✅ Done! Saved {len(note_events)} notes (≥{MIN_NOTE_DURATION:.2f}s) to {OUTPUT_CSV}")


if __name__ == "__main__":
    analyze_mp3_to_csv("songs/nights.mov")
