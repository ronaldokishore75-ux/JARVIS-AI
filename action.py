import webbrowser
import subprocess


def open_google():
    webbrowser.open("https://www.google.com")


def open_youtube():
    webbrowser.open("https://www.youtube.com")


def open_notepad():
    subprocess.Popen("notepad.exe")


def open_calculator():
    subprocess.Popen("calc.exe")

def open_chatgpt():
    webbrowser.open("https://chat.openai.com/")

def open_gemini():
    webbrowser.open("https://www.gemini.com/")
