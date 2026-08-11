import webbrowser
import subprocess
import os
from urllib.parse import quote_plus
from pycaw.pycaw import AudioUtilities
import psutil
from voice import speak
import threading
import time




# COMPUTER CONTROL FUNCTIONS

timer_start_time = None
timer_duration = 0

timer_thread = None
timer_cancel_event = threading.Event()


def start_timer(seconds):

    global timer_thread
    global timer_start_time
    global timer_duration

    # Cancel any previous timer
    timer_cancel_event.clear()

    timer_start_time=time.time()
    timer_duration= seconds

    def timer_worker():

        finished = not timer_cancel_event.wait(seconds)

        if finished:

            print("\n🔔 JARVIS: Your timer is finished!")

            speak("Your timer is finished.")

    timer_thread = threading.Thread(
        target=timer_worker,
        daemon=True
    )

    timer_thread.start()


def get_timer_remaining():

    if timer_thread is None or not timer_thread.is_alive():

        return None

    elapsed = time.time() - timer_start_time

    remaining = timer_duration - elapsed

    if remaining <= 0:

        return None

    return round(remaining)

# =========================================================
# REMINDER
# =========================================================

active_reminders = []
reminder_lock = threading.Lock()


def start_reminder(seconds, message):

    cancel_event = threading.Event()

    reminder = {
        "message": message,
        "cancel_event": cancel_event
    }

    with reminder_lock:
        active_reminders.append(reminder)

    def reminder_worker():

        finished = not cancel_event.wait(seconds)

        with reminder_lock:

            if reminder in active_reminders:
                active_reminders.remove(reminder)

        if finished:

            print(f"\n🔔 JARVIS: Reminder — {message}")

            speak(f"Reminder. {message}")

    reminder_thread = threading.Thread(
        target=reminder_worker,
        daemon=True
    )

    reminder_thread.start()


def cancel_reminder():

    with reminder_lock:

        if not active_reminders:
            return "There are no active reminders."

        reminder = active_reminders.pop(0)

        reminder["cancel_event"].set()

    return "Reminder cancelled."


def list_reminders():

    with reminder_lock:

        count = len(active_reminders)

    if count == 0:
        return "You have no active reminders."

    if count == 1:
        return "You have 1 active reminder."

    return f"You have {count} active reminders."


def cancel_timer():

    if timer_thread is None or not timer_thread.is_alive():

        return "There is no active timer."

    timer_cancel_event.set()

    return "Timer cancelled."  



def get_cpu_usage():

    cpu = psutil.cpu_percent(interval=1)
    return f"CPU usage is {cpu} percent."


def get_ram_usage():
    memory = psutil.virtual_memory()

    used = memory.used / (1024 ** 3)
    total = memory.total / (1024 ** 3)
    percent = memory.percent

    return (
        f"RAM usage is {percent} percent. "
        f"You are using {used:.1f} gigabytes "
        f"out of {total:.1f} gigabytes."
    )


def get_storage_usage():

    disk = psutil.disk_usage("C:\\")

    used = disk.used / (1024 ** 3)
    total = disk.total / (1024 ** 3)
    free = disk.free / (1024 ** 3)

    return (
        f"Your C drive is {disk.percent} percent full. "
        f"You have {free:.1f} gigabytes free "
        f"out of {total:.1f} gigabytes."
    )


def get_battery_level():

    battery = psutil.sensors_battery()

    if battery is None:
        return "I can't detect a battery on this computer."

    percent = battery.percent

    if battery.power_plugged:
        return f"Battery is at {percent} percent and the computer is plugged in."

    return f"Battery is at {percent} percent."


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


def set_volume(percent):

    volume = get_volume_controller()

    percent = max(0, min(percent, 100))

    level = percent / 100.0

    volume.SetMasterVolumeLevelScalar(
        level,
        None
    )

    return f"Volume set to {percent} percent."


def get_current_volume():

    volume = get_volume_controller()

    current = volume.GetMasterVolumeLevelScalar()

    percent = round(current * 100)

    return f"The current volume is {percent} percent."


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