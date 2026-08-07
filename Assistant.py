from voice import speak
from brain import jarvis_response
import subprocess

while True:
    input("\nPress ENTER and speak...")

    subprocess.run(["python", "speech-text.py"])

    with open("command.txt", "r") as file:
        command = file.read().strip()

    print("You:", command)

    if command.lower() == "bye":
        speak("Goodbye!")
        break

    response = jarvis_response(command)
    speak(response)