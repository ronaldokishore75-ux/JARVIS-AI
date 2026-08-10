import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import numpy as np
import noisereduce as nr

model = whisper.load_model("small")

duration = 5
sample_rate = 48000
device = 12


def listen():

    print("🎤 Speak now...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
        device=device
    )

    sd.wait()

    audio = recording.flatten()

    # Remove background noise
    print("🔇 Removing background noise...")

    cleaned_audio = nr.reduce_noise(
        y=audio,
        sr=sample_rate,
        stationary=True,
        prop_decrease=0.8
    )

    # Normalize audio
    max_volume = np.max(np.abs(cleaned_audio))

    if max_volume > 0:
        cleaned_audio = cleaned_audio / max_volume

    # Convert to WAV
    audio_int16 = (
        cleaned_audio * 32767
    ).astype(np.int16)

    write(
        "voice.wav",
        sample_rate,
        audio_int16
    )

    print("🧠 Processing...")

    result = model.transcribe(
        "voice.wav",
        language="en",
        fp16=False,
        initial_prompt=(
            "Jarvis, hey Jarvis, okay Jarvis, "
            "wake up, stop, wait, go to sleep, "
            "stop listening, my name is Kishore."
        )
    )

    text = result["text"].strip()

    print("Whisper:", text)

    return text