import pyglet
import queue
import sys
from pathlib import Path
import time

sys.path.append(str(Path(__file__).resolve().parent.parent / "backend" / "sound_input"))

import live_input

live_input.start_audio_thread()

window = pyglet.window.Window(800,400, caption="Live Note Detection Test")

label = pyglet.text.Label(
    "Listening...",
    font_size=36,
    x=window.width // 2,
    y=window.height // 2,
    anchor_x = "center",
    anchor_y = "center"
)

latest_note_time = 0

def update (dt):
    global latest_note_time
    try:
        while True:
            note_event = live_input.note_queue.get_nowait()
            label.text = f"Note: {note_event['note']} ({note_event['duration']:.2f}s)"
            latest_note_time = note_event['timestamp']
    except queue.Empty:
        # no note for 2 seconds -> show listening
        if time.time() - latest_note_time > 2:
            label.text = "Listening..."
        pass

@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.clock.schedule_interval(update, 1/30.0) # 30fps
pyglet.app.run()

live_input.stop_audio()
print("Audio Stopped.")