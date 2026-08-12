import webbrowser
import subprocess
import os
from datetime import datetime
from urllib.parse import quote_plus
from pycaw.pycaw import AudioUtilities
import psutil
from voice import speak
import threading
import time
import pyautogui
import pytesseract
from browser_controller import browser_controller


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)



# =========================================================
# SCREENSHOT
# =========================================================



def take_screenshot():

    screenshots_folder = os.path.join(
        os.path.dirname(__file__),
        "screenshots"
    )

    os.makedirs(
        screenshots_folder,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    filename = f"screenshot_{timestamp}.png"

    filepath = os.path.join(
        screenshots_folder,
        filename
    )

    screenshot = pyautogui.screenshot()

    screenshot.save(filepath)

    print(f"Screenshot saved: {filepath}")

    return filepath

# =========================================================
# OPEN LAST SCREENSHOT
# =========================================================

def open_last_screenshot():

    screenshots_folder = os.path.join(
        os.path.dirname(__file__),
        "screenshots"
    )

    if not os.path.exists(screenshots_folder):
        return False

    files = [
        os.path.join(screenshots_folder, file)
        for file in os.listdir(screenshots_folder)
        if file.lower().endswith(".png")
    ]

    if not files:
        return False

    latest_file = max(
        files,
        key=os.path.getmtime
    )

    print(f"Opening screenshot: {latest_file}")

    os.startfile(latest_file)

    return True






# =========================================================
# MEDIA PLAY / PAUSE
# =========================================================

def play_pause_media():

    print("Toggling play/pause...")

    pyautogui.press("space")


# =========================================================
# NEXT VIDEO
# =========================================================

def next_video():

    print("Skipping to next video...")

    pyautogui.hotkey("shift", "n")

def previous_video():

    print("Going to previous video...")

    pyautogui.hotkey("shift", "p")


def youtube_mute():

    print("Muting YouTube...")

    pyautogui.press("m")

def youtube_unmute():

    print("Unmuting YouTube...")

    pyautogui.press("m")


# =========================================================
# MEDIA SEEK
# =========================================================

def seek_forward_10():
    print("Skipping forward 10 seconds...")
    
    for _ in range(1):
        pyautogui.press("right")


def seek_backward_10():
    print("Skipping backward 10 seconds...")
    
    for _ in range(1):
        pyautogui.press("left")


def seek_forward_30():
    print("Skipping forward 30 seconds...")
    
    for _ in range(3):
        pyautogui.press("right")
        time.sleep(0.1)


def seek_backward_30():
    print("Skipping backward 30 seconds...")
    
    for _ in range(3):
        pyautogui.press("left")
        time.sleep(0.1)

# =========================================================
# BROWSER SEARCH
# =========================================================

def search_browser(query):

    print(f"Searching for: {query}")

    # Focus browser address/search bar
    pyautogui.hotkey("ctrl", "l")

    time.sleep(0.5)

    # Type the search query
    pyautogui.write(query, interval=0.03)

    time.sleep(0.5)

    # Search
    pyautogui.press("enter")

# =========================================================
# PLAYWRIGHT GOOGLE SEARCH
# =========================================================

def search_google(query):

    print(f"Searching Google for: {query}")

    browser_controller.search_google(query)


# =========================================================
# PLAYWRIGHT YOUTUBE SEARCH
# =========================================================

def open_youtube():

    print("Opening YouTube...")

    browser_controller.open_youtube()


# =========================================================
# CLICK LINK BY NAME
# =========================================================

def click_link_by_name(link_name):

    print(f"Looking for: {link_name}")

    max_scroll_attempts = 5

    for attempt in range(max_scroll_attempts + 1):

        print(
            f"Search attempt "
            f"{attempt + 1}/{max_scroll_attempts + 1}"
        )

        screenshot = pyautogui.screenshot()

        data = pytesseract.image_to_data(
            screenshot,
            output_type=pytesseract.Output.DICT
        )

        target_words = set(
            link_name.lower().strip().split()
        )

        lines = {}

        for i, text in enumerate(data["text"]):

            text = text.lower().strip()

            if not text:
                continue

            line_id = (
                data["block_num"][i],
                data["par_num"][i],
                data["line_num"][i]
            )

            if line_id not in lines:

                lines[line_id] = {
                    "words": [],
                    "left": [],
                    "top": [],
                    "right": [],
                    "bottom": []
                }

            lines[line_id]["words"].append(text)

            lines[line_id]["left"].append(
                data["left"][i]
            )

            lines[line_id]["top"].append(
                data["top"][i]
            )

            lines[line_id]["right"].append(
                data["left"][i] + data["width"][i]
            )

            lines[line_id]["bottom"].append(
                data["top"][i] + data["height"][i]
            )

        best_match = None
        best_score = 0

        for line in lines.values():

            line_words = set(line["words"])

            matched_words = target_words.intersection(
                line_words
            )

            score = len(matched_words)

            if score > best_score:

                best_score = score
                best_match = line

        # ---------------------------------------------
        # MATCH FOUND
        # ---------------------------------------------

        if best_match and best_score > 0:

            left = min(best_match["left"])
            top = min(best_match["top"])
            right = max(best_match["right"])
            bottom = max(best_match["bottom"])

            click_x = (left + right) // 2
            click_y = (top + bottom) // 2

            found_text = " ".join(
                best_match["words"]
            )

            print(
                f"Found match: {found_text}"
            )

            print(
                f"Match score: {best_score}"
            )

            print(
                f"Clicking at: "
                f"{click_x}, {click_y}"
            )

            pyautogui.moveTo(
                click_x,
                click_y,
                duration=0.5
            )

            pyautogui.click()

            return True

        # ---------------------------------------------
        # NOT FOUND — SCROLL
        # ---------------------------------------------

        if attempt < max_scroll_attempts:

            print(
                "No match found. "
                "Scrolling down..."
            )

            pyautogui.scroll(-5)

            time.sleep(1.5)

    print(
        f"Could not find '{link_name}' "
        "after scrolling."
    )

    return False

def skip_ad():

    possible_names = [
        "skip ad",
        "skip ads",
        "skip"
    ]

    for name in possible_names:

        print(f"Trying to find: {name}")

        if click_link_by_name(name):
            print("Ad skipped.")
            return True

    print("Skip button not found.")

    return False

def full_screen():

    print("Entering full screen...")

    pyautogui.press("f")

    return True


def exit_full_screen():

    print("Exiting full screen...")

    pyautogui.press("esc")

    return True

# =========================================================
# BROWSER SCROLL
# =========================================================

def scroll_down():

    print("Scrolling down...")

    browser_controller.scroll_down()


def scroll_up():

    print("Scrolling up...")

    browser_controller.scroll_up()


def scroll_down_little():

    print("Scrolling down a little...")

    browser_controller.scroll_down_little()


def scroll_up_little():

    print("Scrolling up a little...")

    browser_controller.scroll_up_little()

# =========================================================
# BROWSER NAVIGATION
# =========================================================

def go_back():

    print("Going back...")

    pyautogui.hotkey("alt", "left")


def go_forward():

    print("Going forward...")

    pyautogui.keyDown("alt")
    time.sleep(0.2)

    pyautogui.press("right")

    time.sleep(0.2)

    pyautogui.keyUp("alt")


def refresh_page():

    print("Refreshing page...")

    pyautogui.hotkey("ctrl", "r")

def open_new_tab():

    print("Opening new tab...")

    pyautogui.hotkey("ctrl", "t")



def close_current_tab():

    print("Closing current tab...")

    pyautogui.hotkey("ctrl", "w")

def next_tab():

    print("Switching to next tab...")

    pyautogui.hotkey("ctrl", "tab")

def previous_tab():

    print("Switching to previous tab...")

    pyautogui.hotkey("ctrl", "shift", "tab")

# =========================================================
# WINDOW CONTROL
# =========================================================

def show_desktop():

    print("Showing desktop...")

    pyautogui.hotkey("win", "d")


def minimize_window():

    print("Minimizing current window...")

    pyautogui.hotkey("alt", "space")
    time.sleep(0.3)
    pyautogui.press("n")


def maximize_window():

    print("Maximizing current window...")


    pyautogui.hotkey("alt", "space")
    time.sleep(0.3)
    pyautogui.press("x")


def restore_window():

    print("Restoring current window...")


    pyautogui.hotkey("alt", "space")
    time.sleep(0.3)
    pyautogui.press("r")


def close_window():

    print("Closing current window...")

    pyautogui.hotkey("alt", "f4")


def sleep_computer():

    print("Putting computer to sleep...")

    subprocess.run(
        [
            "rundll32.exe",
            "powrprof.dll,SetSuspendState",
            "0,1,0"
        ]
    )



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

    print("Opening YouTube in JARVIS browser...")

    browser_controller.open_youtube()


def search_youtube(query):

    print(f"Searching YouTube for: {query}")

    browser_controller.search_youtube(query)


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