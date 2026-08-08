import sounddevice as sd
from scipy.io.wavfile import write
import whisper

model = whisper.load_model("base")

duration = 5
sample_rate = 48000
device = 12     # Your microphone index


def listen():

    print("🎤 Speak now...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
    )

    sd.wait()

    write("voice.wav", sample_rate, recording)

    print("🧠 Processing...")

    result = model.transcribe("voice.wav")

    return result["text"]
