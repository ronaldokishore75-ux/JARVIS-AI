import webbrowser
import subprocess
import os
from urllib.parse import quote_plus
from pycaw.pycaw import AudioUtilities


# =========================================================
# AUDIO
# =========================================================

def get_volume_controller():
    device = AudioUtilities.GetSpeakers()

    return device.EndpointVolume   


def volume_up():
    volume = get_volume_controller()

    current = volume.GetMasterVolumeLevelScalar()

    new_volume = min(current + 0.10, 1.0)

    volume.SetMasterVolumeLevelScalar(
        new_volume,
        None
    )


def volume_down():
    volume = get_volume_controller()

    current = volume.GetMasterVolumeLevelScalar()

    new_volume = max(current - 0.10, 0.0)

    volume.SetMasterVolumeLevelScalar(
        new_volume,
        None
    )


def mute_volume():
    volume = get_volume_controller()

    volume.SetMute(1, None)


def unmute_volume():
    volume = get_volume_controller()

    volume.SetMute(0, None)


# =========================================================
# GOOGLE
# =========================================================

def open_google():
    webbrowser.open("https://www.google.com")


def search_google(query):
    url = f"https://www.google.com/search?q={quote_plus(query)}"
    webbrowser.open(url)


# =========================================================
# YOUTUBE
# =========================================================

def open_youtube():
    webbrowser.open("https://www.youtube.com")


def search_youtube(query):
    url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
    webbrowser.open(url)


# =========================================================
# WINDOWS APPLICATIONS
# =========================================================

def open_notepad():
    print("DEBUG: Launching Notepad...")
    os.startfile("notepad.exe")


def open_calculator():
    print("DEBUG: Launching Calculator...")
    subprocess.Popen("calc.exe")

def lock_computer():
    subprocess.run(
        ["rundll32.exe", "user32.dll,LockWorkStation"]
    )

def open_vscode():
    subprocess.Popen(
        ["code"],
        shell=True
    )


def open_file_explorer():
    subprocess.Popen("explorer.exe")


def open_powershell():
    subprocess.Popen(
        ["powershell.exe"],
        shell=True
    )


def open_command_prompt():
    subprocess.Popen(
        ["cmd.exe"],
        shell=True
    )


def open_downloads():
    downloads = os.path.join(
        os.path.expanduser("~"),
        "Downloads"
    )

    os.startfile(downloads)

def close_notepad():
    result = subprocess.run(
        ["taskkill", "/F", "/IM", "notepad.exe"],
        capture_output=True,
        text=True
    )

    print("Notepad close:", result.stdout.strip())
    print("Notepad error:", result.stderr.strip())


def close_calculator():
    result = subprocess.run(
        ["taskkill", "/F", "/IM", "CalculatorApp.exe"],
        capture_output=True,
        text=True
    )

    print("Calculator close:", result.stdout.strip())
    print("Calculator error:", result.stderr.strip())


# =========================================================
# JARVIS PROJECT
# =========================================================

def open_jarvis_folder():
    os.startfile(r"D:\jarvis")


def open_jarvis_vscode():
    subprocess.Popen(
        ["code", r"D:\jarvis"],
        shell=True
    )


# =========================================================
# CHATGPT / GEMINI
# =========================================================

def open_chatgpt():
    webbrowser.open("https://chat.openai.com/")


def open_gemini():
    webbrowser.open("https://gemini.google.com/")