from brain import jarvis_response
from whisper_ai import listen
from voice import speak
import string

print("=" * 50)
print("           JARVIS AI")
print("=" * 50)

name = "Kishore"

speak(f"Welcome, {name}")

while True:

    # Wait for wake word
    print("🎤 Waiting for wake word...")
    wake_word = listen()

    wake_word = wake_word.lower().translate(
        str.maketrans("", "", string.punctuation)
    )

    print("Wake word:", wake_word)

    # Exit anytime
    if "bye" in wake_word:
        speak("Goodbye!")
        break

    # Wake Jarvis
    if "jarvis" not in wake_word:
        continue

    speak("Yes?")

    # Listen for command
    command = listen()
    print("Command:", command)

    if "bye" in command.lower():
        speak("Goodbye!")
        break

    # Process command
    response = jarvis_response(command)

    print("JARVIS:", response)
    speak(response)