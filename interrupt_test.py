import sounddevice as sd
import numpy as np

duration = 5
sample_rate = 48000
device = 12

print("🎤 Speak now!")

recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="float32",
    device=device
)

sd.wait()

volume = np.max(np.abs(recording))

print("Microphone level:", volume)

if volume > 0.01:
    print("🎤 Microphone detected your voice!")
else:
    print("🔇 No voice detected.")