import pyglet
import time
import sys

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend" / "sound_input"))

import live_input

window = pyglet.window.Window(800, 400, caption=" Audio Input")
label = pyglet.text.Label("Listening...", font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x="center", anchor_y="center")

# Start listening once
live_input.start_listening()

def update(dt):
    note = live_input.get_latest_note()
    label.text = f"Note: {note}" if note else "Listening..."

@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.clock.schedule_interval(update, 1/30)
pyglet.app.run()
live_input.stop_listening()
