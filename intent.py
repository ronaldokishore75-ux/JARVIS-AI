import re


def detect_intent(command):

    command = command.lower().strip()

    # =========================================================
    # NOTHING FOUND
    # =========================================================


    #==========================================================

    #computer function

 


    # =========================================================
    # TIMER
    # =========================================================



    timer_pattern = r"(?:set|start)\s+(?:a\s+)?timer\s+for\s+(\d+)\s+(second|seconds|minute|minutes|hour|hours)"

    match = re.fullmatch(timer_pattern, command)

    if match:
        amount = int(match.group(1))
        unit = match.group(2)

        if unit.startswith("second"):
            seconds = amount

        elif unit.startswith("minute"):
            seconds = amount * 60

        elif unit.startswith("hour"):
            seconds = amount * 60 * 60

        else:
            seconds = amount
        return "set_timer", seconds


    # =========================================================
    # CANCEL TIMER
    # =========================================================

    cancel_timer_patterns = [

        r"cancel timer",
        r"cancel the timer",
        r"cancel my timer",

        r"stop timer",
        r"stop the timer",
        r"stop my timer",

    # Whisper variations
        r"cancel time",
        r"cancel the time",
        r"cancel my time",
        r"stop time",
        r"stop the time",
        r"stop my time",
        r"stop time over",
        ]

    for pattern in cancel_timer_patterns:

        if re.fullmatch(pattern, command):

            return "cancel_timer", None


   # =========================================================
   # TIMER REMAINING
   # =========================================================

    timer_remaining_patterns = [

       
        r"how much time is left",
        r"how much time is remaining",
        r"how much time remains",
        r"how long is left",
        r"how long is remaining",
        r"how long is left on my timer",
        r"how much time is left on my timer",
        r"how much time is remaining on my timer",
        r"check my timer",
        r"check the timer",
        ]

    for pattern in timer_remaining_patterns:

        if re.fullmatch(pattern, command):

            return "timer_remaining", None 


    # =========================================================
    # REMINDER
    # =========================================================

    reminder_pattern = re.fullmatch(
        r"remind me in (\d+) (seconds?|minutes?|hours?)"
        r"(?: to (.+))?",
        command
        )

    if reminder_pattern:
        amount = int(reminder_pattern.group(1))
        unit = reminder_pattern.group(2)
        message = reminder_pattern.group(3)

        if unit.startswith("second"):
            seconds = amount

        elif unit.startswith("minute"):
            seconds = amount * 60

        elif unit.startswith("hour"):
            seconds = amount * 60 * 60

        else:
            seconds = amount

        if message:
            message = message.strip()
        else:
            message = "Your reminder"

        return "set_reminder", (seconds, message)


    #=========================================================
    #CANCEL REMAINDER
    #===================================


    cancel_reminder_patterns = [
        r"cancel reminder",
        r"cancel the reminder",
        r"cancel my reminder",
        r"stop reminder",
        r"stop the reminder",
        r"stop my reminder",
        ]

    for pattern in cancel_reminder_patterns:

        if re.fullmatch(pattern, command):

            return "cancel_reminder", None



    # =========================================================
    # LIST REMINDERS
    # =========================================================

    list_reminder_patterns = [
        r"what reminders do i have",
        r"show my reminders",
        r"list my reminders",
        r"check my reminders",
        r"check reminders",
    ]

    for pattern in list_reminder_patterns:

        if re.fullmatch(pattern, command):

            return "list_reminders", None


    # =========================================================
    # CPU USAGE
    # =========================================================

    cpu_patterns = [
        r"what is my cpu usage",
        r"what's my cpu usage",
        r"how much cpu am i using",
        r"check cpu usage",
        r"check my cpu",
        r"cpu usage",
        ]
    for pattern in cpu_patterns:

        if re.fullmatch(pattern, command):
            return "cpu_usage", None


    # =========================================================
    # RAM USAGE
    # =========================================================

    ram_patterns = [
       r"what is my ram usage",
       r"what's my ram usage",
       r"how much ram am i using",
       r"check ram usage",
       r"check my ram",
       r"ram usage",
       r"memory usage",
       ]

    for pattern in ram_patterns:
        if re.fullmatch(pattern, command):
            return "ram_usage", None


    # =========================================================
    # STORAGE
    # =========================================================

    storage_patterns = [
        r"how much storage do i have",
        r"check my storage",
        r"check storage",
        r"how much space do i have",
        r"how much disk space do i have",
        r"check disk space",
        r"disk usage",
        r"storage usage"
        ]

    for pattern in storage_patterns:
        if re.fullmatch(pattern, command):

            return "storage_usage", None


    # =========================================================
    # BATTERY
    # =========================================================

    battery_patterns = [
       r"what is my battery level",
       r"what's my battery level",
       r"how much battery do i have",
       r"check my battery",
       r"check battery",
       r"battery level",
       r"battery",
       ]

    for pattern in battery_patterns:

        if re.fullmatch(pattern, command):
            return "battery_level", None
    
    # =========================================================
    # VOLUME UP
    # =========================================================

    volume_up_patterns = [
        r"volume\s+up",
        r"turn\s+(?:the\s+)?volume\s+up",
        r"increase\s+(?:the\s+)?volume",
        r"make\s+(?:the\s+)?volume\s+louder",
        r"make\s+it\s+louder",
        ]

    for pattern in volume_up_patterns:
        if re.fullmatch(pattern, command):

            return "volume_up", None


    # =========================================================
    # VOLUME DOWN
    # =========================================================

    volume_down_patterns = [
        r"volume\s+down",
        r"turn\s+(?:the\s+)?volume\s+down",
        r"decrease\s+(?:the\s+)?volume",
        r"make\s+(?:the\s+)?volume\s+quieter",
        r"make\s+it\s+quieter",
        ]

    for pattern in volume_down_patterns:

        if re.fullmatch(pattern, command):
            return "volume_down", None


    # =========================================================
    # MUTE
    # =========================================================

    mute_patterns = [
        r"mute",
        r"mute\s+(?:the\s+)?volume",
        r"mute\s+(?:the\s+)?sound"
        ]

    for pattern in mute_patterns:
        if re.fullmatch(pattern, command):

            return "mute_volume", None


    # =========================================================
    # UNMUTE
    # =========================================================

    unmute_patterns = [
        r"unmute",
        r"unmute\s+(?:the\s+)?volume",
        r"unmute\s+(?:the\s+)?sound",
        ]

    for pattern in unmute_patterns:

        if re.fullmatch(pattern, command):

            return "unmute_volume", None


    # =========================================================
    # SET VOLUME
    # =========================================================


    volume_set_patterns = [
        r"set\s+(?:the\s+|my\s+)?volume\s+to\s+(\d+)\s*(?:percent|%)?",
        r"set\s+(?:the\s+|my\s+)?volume\s+(?:at|on)\s+(\d+)\s*(?:percent|%)?",
        r"change\s+(?:the\s+|my\s+)?volume\s+to\s+(\d+)\s*(?:percent|%)?",
        r"change\s+(?:the\s+|my\s+)?volume\s+(?:at|on)\s+(\d+)\s*(?:percent|%)?",
        r"volume\s+(\d+)\s*(?:percent|%)?",
        ]

    for pattern in volume_set_patterns:

        match = re.fullmatch(pattern, command)

        if match:

            percent = int(match.group(1))

            # Keep volume between 0 and 100
            
            percent = max(0, min(percent, 100))

            return "set_volume", percent


    # =========================================================
    # CURRENT VOLUME
    # =========================================================

    current_volume_patterns = [

        r"what is (?:the\s+|my\s+)?current volume",
        r"what's (?:the\s+|my\s+)?current volume",
        r"what is (?:the\s+|my\s+)?current volume level",
        r"what's (?:the\s+|my\s+)?current volume level",
        r"what is (?:the\s+|my\s+)?volume",
        r"what's (?:the\s+|my\s+)?volume",
        r"what is (?:the\s+|my\s+)?volume level",
        r"what's (?:the\s+|my\s+)?volume level",
        r"check (?:the\s+|my\s+)?volume",
        r"check (?:the\s+|my\s+)?volume level",
        r"current volume",
        r"current volume level",
        ]

    for pattern in current_volume_patterns:

        if re.fullmatch(pattern, command):

            return "get_current_volume", None

    # =========================================================
    # LOCK COMPUTER
    # =========================================================

    lock_patterns = [
        r"lock\s+(?:the\s+)?computer",
        r"lock\s+(?:my\s+)?computer",
        r"lock\s+(?:the\s+)?pc",
        r"lock\s+(?:my\s+)?pc",
        r"lock\s+windows",
        ]

    for pattern in lock_patterns:

        if re.fullmatch(pattern, command):
            return "lock_computer", None
    # =========================================================
    # OPEN GOOGLE
    # =========================================================

    google_open_patterns = [
        r"open\s+(?:the\s+)?google",
        r"launch\s+(?:the\s+)?google",
        r"start\s+(?:the\s+)?google",
        r"bring\s+up\s+(?:the\s+)?google",
    ]

    for pattern in google_open_patterns:
        if re.fullmatch(pattern, command):
            return "open_google", None

    # =========================================================
    # OPEN YOUTUBE
    # =========================================================

    youtube_open_patterns = [
        r"open\s+(?:the\s+)?youtube",
        r"launch\s+(?:the\s+)?youtube",
        r"start\s+(?:the\s+)?youtube",
        r"bring\s+up\s+(?:the\s+)?youtube",
    ]

    for pattern in youtube_open_patterns:
        if re.fullmatch(pattern, command):
            return "open_youtube", None

    # =========================================================
    # OPEN NOTEPAD
    # =========================================================

    notepad_open_patterns = [
        r"open\s+(?:the\s+)?notepad",
        r"launch\s+(?:the\s+)?notepad",
        r"start\s+(?:the\s+)?notepad",
        r"bring\s+up\s+(?:the\s+)?notepad",
        r"open\s+my\s+notepad",
    ]

    for pattern in notepad_open_patterns:
        if re.fullmatch(pattern, command):
            return "open_notepad", None

    # =========================================================
    # OPEN CALCULATOR
    # =========================================================

    calculator_open_patterns = [
        r"open\s+(?:the\s+)?calculator",
        r"open\s+(?:the\s+)?calc",
        r"launch\s+(?:the\s+)?calculator",
        r"start\s+(?:the\s+)?calculator",
        r"bring\s+up\s+(?:the\s+)?calculator",
        r"open\s+my\s+calculator",
    ]

    for pattern in calculator_open_patterns:
        if re.fullmatch(pattern, command):
            return "open_calculator", None

    # =========================================================
    # OPEN VS CODE
    # =========================================================

    vscode_patterns = [
        r"open\s+vscode",
        r"open\s+vs\s+code",
        r"open\s+(?:visual\s+studio\s+code)",
        r"launch\s+vscode",
        r"launch\s+vs\s+code",
        r"start\s+vscode",
        r"start\s+vs\s+code",
    ]

    for pattern in vscode_patterns:
        if re.fullmatch(pattern, command):
            return "open_vscode", None

    # =========================================================
    # OPEN FILE EXPLORER
    # =========================================================

    explorer_patterns = [
        r"open\s+(?:the\s+)?file\s+explorer",
        r"open\s+(?:the\s+)?explorer",
        r"launch\s+(?:the\s+)?file\s+explorer",
        r"start\s+(?:the\s+)?file\s+explorer",
    ]

    for pattern in explorer_patterns:
        if re.fullmatch(pattern, command):
            return "open_file_explorer", None

    # =========================================================
    # OPEN DOWNLOADS
    # =========================================================

    downloads_patterns = [
        r"open\s+downloads",
        r"open\s+my\s+downloads",
        r"open\s+downloads\s+folder",
        r"open\s+my\s+downloads\s+folder",
    ]

    for pattern in downloads_patterns:
        if re.fullmatch(pattern, command):
            return "open_downloads", None

    # =========================================================
    # OPEN POWERSHELL
    # =========================================================

    powershell_patterns = [
        r"open\s+powershell",
        r"launch\s+powershell",
        r"start\s+powershell",
    ]

    for pattern in powershell_patterns:
        if re.fullmatch(pattern, command):
            return "open_powershell", None

    # =========================================================
    # OPEN COMMAND PROMPT
    # =========================================================

    cmd_patterns = [
        r"open\s+(?:the\s+)?command\s+prompt",
        r"open\s+cmd",
        r"launch\s+(?:the\s+)?command\s+prompt",
        r"start\s+(?:the\s+)?command\s+prompt",
    ]

    for pattern in cmd_patterns:
        if re.fullmatch(pattern, command):
            return "open_command_prompt", None

    # =========================================================
    # OPEN JARVIS FOLDER
    # =========================================================

    jarvis_folder_patterns = [
        r"open\s+jarvis\s+folder",
        r"open\s+my\s+jarvis\s+folder",
        r"open\s+my\s+project\s+folder",
        r"open\s+jarvis\s+project\s+folder",
    ]

    for pattern in jarvis_folder_patterns:
        if re.fullmatch(pattern, command):
            return "open_jarvis_folder", None

    # =========================================================
    # OPEN JARVIS IN VS CODE
    # =========================================================

    if (
        "open jarvis in vscode" in command
        or "open jarvis in vs code" in command
        or "open jarvis project in vscode" in command
        or "open jarvis project in vs code" in command
    ):
        return "open_jarvis_vscode", None

    # =========================================================
    # GOOGLE SEARCH
    # =========================================================

    google_search_patterns = [
        r"search google for (.+)",
        r"search google (.+)",
        r"search for (.+) on google",
        r"find (.+) on google",
        r"google (.+)",
    ]

    for pattern in google_search_patterns:

        match = re.fullmatch(pattern, command)

        if match:

            query = match.group(1).strip()

            if query:
                return "search_google", query

    # =========================================================
    # YOUTUBE SEARCH
    # =========================================================

    youtube_search_patterns = [
        r"search youtube for (.+)",
        r"search youtube (.+)",
        r"search for (.+) on youtube",
        r"find (.+) on youtube",
        r"youtube (.+)",
    ]

    for pattern in youtube_search_patterns:

        match = re.fullmatch(pattern, command)

        if match:

            query = match.group(1).strip()

            if query:
                return "search_youtube", query

    # =========================================================
    # CLOSE NOTEPAD
    # =========================================================

    notepad_close_patterns = [
        r"close\s+(?:the\s+)?notepad",
        r"exit\s+(?:the\s+)?notepad",
        r"quit\s+(?:the\s+)?notepad",
    ]

    for pattern in notepad_close_patterns:
        if re.fullmatch(pattern, command):
            return "close_notepad", None

    # =========================================================
    # CLOSE CALCULATOR
    # =========================================================

    calculator_close_patterns = [
        r"close\s+(?:the\s+)?calculator",
        r"close\s+(?:the\s+)?calc",
        r"exit\s+(?:the\s+)?calculator",
        r"quit\s+(?:the\s+)?calculator",
    ]

    for pattern in calculator_close_patterns:
        if re.fullmatch(pattern, command):
            return "close_calculator", None

    # =========================================================
    # NOTHING FOUND
    # =========================================================

    return None, None