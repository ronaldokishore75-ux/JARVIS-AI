import sounddevice as sd
import numpy as np
import time

SAMPLE_RATE = 48000
DEVICE = 12
THRESHOLD = 0.012

consecutive = 0


def microphone_callback(indata, frames, time_info, status):
    global consecutive

    volume = np.max(np.abs(indata))

    if volume > THRESHOLD:
        consecutive += 1
    else:
        consecutive = 0

    if consecutive >= 3:
        print("🛑 VOICE DETECTED!")
        consecutive = 0


print("🎤 Microphone monitoring for 10 seconds...")
print("Stay quiet, then say STOP.")

with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="float32",
    device=DEVICE,
    callback=microphone_callback
):
    time.sleep(10)

print("✅ Test finished.")