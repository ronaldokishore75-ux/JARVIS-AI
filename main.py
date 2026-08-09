from brain import jarvis_response
from whisper_ai import listen
from voice import speak, stop_speaking
import string

print("=" * 50)
print("           JARVIS AI")
print("=" * 50)

name = "Kishore"

speak(f"Welcome, {name}")


# Wake phrases
WAKE_WORDS = [
    "hey",
    "hey jarvis",
    "okay jarvis",
    "ok jarvis",
    "wake up",
    "wake",
    "jarvis"
]


while True:



    print("🎤 Waiting for wake word...")

    wake_word = listen()

    wake_word = wake_word.lower().translate(
        str.maketrans("", "", string.punctuation)
    )

    print("Wake word:", wake_word)

    # Completely exit
    if "bye" in wake_word:
        speak("Goodbye!")
        break

    # Check wake words
    if not any(word in wake_word for word in WAKE_WORDS):
        continue




    if "okay jarvis" in wake_word or "ok jarvis" in wake_word:
        speak("Okay! How can I help you?")

    elif "wake up" in wake_word or wake_word == "wake":
        speak("I am awake and ready to assist you.")

    elif "hey jarvis" in wake_word:
        speak("Hey! How can I help you?")

    else:
        speak("Yes?")


    while True:

        print("🎤 Listening...")

        command = listen()

        command = command.lower().strip()

        print("You:", command)


        # Go back to sleep
        if "go to sleep" in command or "stop listening" in command:
            speak("Okay, I'll wait for you.")
            break


        # Completely exit
        if "bye" in command:
            speak("Goodbye!")
            exit()


        # Process command
        response = jarvis_response(command)

        print("JARVIS:", response)

        speak(response)