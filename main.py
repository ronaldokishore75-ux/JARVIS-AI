from brain import jarvis_response
from whisper_ai import listen
from voice import speak, stop_speaking
import string


print("=" * 50)
print("           JARVIS AI")
print("=" * 50)

name = "Kishore"

speak(f"Welcome, {name}")


# =========================================================
# WAKE WORDS
# =========================================================

WAKE_WORDS = [
    "hey",
    "hey jarvis",
    "okay jarvis",
    "ok jarvis",
    "wake up",
    "wake",
    "jarvis"
]


# =========================================================
# NORMALIZE VOICE INPUT
# =========================================================

def clean_command(text):

    return text.lower().translate(
        str.maketrans("", "", string.punctuation)
    ).strip()


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    print("🎤 Waiting for wake word...")

    wake_word = listen()

    wake_word = clean_command(wake_word)

    print("Wake word:", wake_word)


    # =====================================================
    # EXIT FROM WAKE MODE
    # =====================================================

    if "bye" in wake_word:

        speak("Goodbye!")

        break


    # =====================================================
    # CHECK WAKE WORD
    # =====================================================

    if not any(
        word in wake_word
        for word in WAKE_WORDS
    ):

        continue


    # =====================================================
    # WAKE RESPONSE
    # =====================================================

    if (
        "okay jarvis" in wake_word
        or "ok jarvis" in wake_word
    ):

        speak("Okay! How can I help you?")

    elif (
        "wake up" in wake_word
        or wake_word == "wake"
    ):

        speak(
            "I am awake and ready to assist you."
        )

    elif "hey jarvis" in wake_word:

        speak(
            "Hey! How can I help you?"
        )

    else:

        speak("Yes?")


    # =====================================================
    # ACTIVE CONVERSATION
    # =====================================================

    while True:

        print("🎤 Listening...")

        command = listen()

        command = clean_command(command)

        print("You:", command)


        # =================================================
        # IGNORE EMPTY INPUT
        # =================================================

        if not command:

            continue


        # =================================================
        # GO TO SLEEP
        # =================================================

        if (
            "go to sleep" in command
            or "stop listening" in command
        ):

            speak("Okay, I'll wait for you.")

            break


        # =================================================
        # EXIT JARVIS
        # =================================================

        if command == "bye":

            speak("Goodbye!")

            raise SystemExit


        # =================================================
        # STOP SPEAKING
        #
        # IMPORTANT:
        # Only exact stop commands are handled here.
        # We do NOT use:
        #
        #     "stop" in command
        #
        # because that can interfere with other commands.
        # =================================================

        if command in [
            "stop",
            "stop talking",
            "jarvis stop",
            "stop speaking",
            "be quiet",
            "quiet",
            "wait",
        ]:

            print("🛑 Stop command received.")

            stop_speaking()

            continue


        # =================================================
        # SEND EVERYTHING ELSE TO BRAIN
        # =================================================

        response = jarvis_response(command)


        # =================================================
        # SPEAK RESPONSE
        # =================================================

        speak(response)