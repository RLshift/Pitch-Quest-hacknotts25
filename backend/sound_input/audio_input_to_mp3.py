import pyaudio
import wave
from pydub import AudioSegment
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10
WAV_FILENAME = "output.wav"
MP3_FILENAME = "output.mp3"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Start Recording...")

frames = []
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording Stopped")

stream.stop_stream()
stream.close()
p.terminate()

# Save to WAV first
wf = wave.open(WAV_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

# Convert to MP3
sound = AudioSegment.from_wav(WAV_FILENAME)
sound.export(MP3_FILENAME, format="mp3")

os.remove(WAV_FILENAME)

print(f"Saved recording as {MP3_FILENAME}")
