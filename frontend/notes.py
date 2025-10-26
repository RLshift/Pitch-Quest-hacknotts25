import csv
from pathlib import Path
import math

_csv_files = {
    "nights": Path("../backend/notes/output/nights.csv"),
    "stargazing": Path("../backend/notes/output/stargazing.csv"),
    "dont_stop": Path("../backend/notes/output/dont_stop.csv"),
    "coulda_been_me": Path("../backend/notes/output/coulda_been_me.csv"),
    "kilby_girl": Path("../backend/notes/output/kilby_girl.csv"),
}

def _load_notes(csv_path: Path):
    notes = []
    if csv_path.exists():
        with open (csv_path, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                note = row.get("note_name")
                if note:
                    notes.append(note)
    else:
        print("missing a csv file")
    return notes

def freq_to_note(freq, A4=440.0):
    if freq <= 0:
        return None
    
    midi = 69 + 12 * math.log2(freq / A4)
    midi_int = int(round(midi))
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
    name = note_names[midi_int % 12] + str(midi_int // 12 - 1)
    return name

def getNotes(song_name: str):
    song_name = song_name.lower().strip()
    if song_name not in _csv_files:
        print("Unknown Song")
    return _load_notes(_csv_files[song_name])

def checkNotes(notes_array, hz, tolerance = 0):
    note_name = freq_to_note(hz)
    if note_name is None:
        return False
    
    return note_name in notes_array