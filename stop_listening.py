import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import threading
import os

MODEL = whisper.load_model("base")

DEVICE = 12
SAMPLE_RATE = 48000
DURATION = 2

STOP_WORDS = [
    "stop",
    "wait",
    "jarvis stop",
]


def listen_for_stop():
    print("🎤 Listening for STOP...")

    recording = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        device=DEVICE,
    )

    sd.wait()

    filename = "stop_check.wav"
    write(filename, SAMPLE_RATE, recording)

    result = MODEL.transcribe(
        filename,
        fp16=False
    )

    text = result["text"].lower().strip()

    print("Heard:", text)

    # Delete temporary recording
    if os.path.exists(filename):
        os.remove(filename)

    for word in STOP_WORDS:
        if word in text:
            return True

    return False


if __name__ == "__main__":

    print("================================")
    print("     STOP WORD TEST")
    print("================================")

    result = listen_for_stop()

    if result:
        print("🛑 STOP COMMAND DETECTED!")
    else:
        print("❌ No stop command detected.")