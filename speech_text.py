import sounddevice as sd
from scipy.io.wavfile import write
import whisper

# Load Whisper model
model = whisper.load_model("base")

# Recording settings
duration = 5
sample_rate = 48000
device = 12  # Your microphone index

print("🎤 Speak now...")

recording = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16",
    device=device
)

sd.wait()

write("voice.wav", sample_rate, recording)

print("🧠 Processing...")

result = model.transcribe("voice.wav")

print("You said:")
print(result["text"])
with open("command.txt", "w") as file:
    file.write(result["text"])