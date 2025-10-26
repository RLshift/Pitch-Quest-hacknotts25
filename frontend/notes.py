import csv
from pathlib import Path

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

def getNotes(song_name: str):
    song_name = song_name.lower().strip()
    if song_name not in _csv_files:
        print("Unknown Song")
    return _load_notes(_csv_files[song_name])

notes = getNotes("kilby_girl")

print(notes)