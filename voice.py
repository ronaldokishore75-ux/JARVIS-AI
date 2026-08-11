import pyttsx3




def speak(text):
    
    print("JARVIS:", text)

    engine = pyttsx3.init()


    engine.setProperty("rate", 170)

    voices = engine.getProperty("voices")

    if voices:
        engine.setProperty("voice", voices[0].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()


def stop_speaking():
    pass