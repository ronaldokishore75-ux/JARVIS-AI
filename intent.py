import re


def detect_intent(command):

    command = command.lower().strip()


    command=re.sub(
        r"[.!?]+$",
        "",
        command
    ).strip()

    # =========================================================
    # NOTHING FOUND
    # =========================================================


    #==========================================================

    #computer function


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
    # V5 TASK STATUS
    # =========================================================

    task_status_commands = {
        "task status",
        "what is the task status",
        "what's the task status",
        "is the task finished",
        "is the task done",
        "what task are you doing",
        "what are you doing",
        "what step are you on",
     "which step are you on",
    }

    if command in task_status_commands:

        return "task_status", None



    # =========================================================
    # CANCEL CURRENT TASK
    # =========================================================

    if command in [
        "stop task",
        "stop the task",
        "cancel task",
        "cancel the task",
        "stop this task",
        "cancel this task",
        "abort task",
        "abort the task",
    ]:
        return "cancel_task", None






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
    # WINDOW CONTROL
    # =========================================================

    minimize_window_patterns = [
        r"minimize this window",
        r"minimize the window",
        r"minimize window",
        r"minimize these windows",
    ]

    for pattern in minimize_window_patterns:
        if re.fullmatch(pattern, command):
            return "minimize_window", None


    maximize_window_patterns = [
        r"maximize this window",
        r"maximize the window",
        r"maximize window",
    ]

    for pattern in maximize_window_patterns:
        if re.fullmatch(pattern, command):
            return "maximize_window", None


    restore_window_patterns = [
        r"restore this window",
        r"restore the window",
        r"restore window",
    ]

    for pattern in restore_window_patterns:
        if re.fullmatch(pattern, command):
            return "restore_window", None


    close_window_patterns = [
        r"close this window",
        r"close the window",
        r"close window",
    ]

    for pattern in close_window_patterns:
        if re.fullmatch(pattern, command):
            return "close_window", None


    # =========================================================
    # SLEEP COMPUTER
    # =========================================================

    sleep_computer_patterns = [
        r"sleep computer",
        r"sleep the computer",
        r"put the computer to sleep",
        r"put my computer to sleep",
        r"go to sleep",
    ]

    for pattern in sleep_computer_patterns:

        if re.fullmatch(pattern, command):
            return "sleep_computer", None



  


    # =========================================================
    # GO BACK
    # =========================================================

    go_back_patterns = [
        r"go back",
        r"go back to previous page",
        r"previous page",
        r"go to the previous page",
    ]

    for pattern in go_back_patterns:

        if re.fullmatch(pattern, command):
            return "go_back", None


    # =========================================================
    # SHOW DESKTOP
    # =========================================================

    show_desktop_patterns = [
        r"show desktop",
        r"show the desktop",
        r"go to desktop",
    ]

    for pattern in show_desktop_patterns:
        if re.fullmatch(pattern, command):
            return "show_desktop", None

        
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
    # PLAY / PAUSE MEDIA
    # =========================================================

    if command in [
        "play",
        "pause",
        "play video",
        "pause video",
        "resume",
        "resume video",
    ]:
        return "play_pause_media", None


    



    # =========================================================
    # NEXT VIDEO
    # =========================================================

    if command in [
        "next video",
        "skip to next video",
        "play next video",
        "go to next video",
    ]:
        return "next_video", None


    # =========================================================
    # PREVIOUS VIDEO
    # =========================================================

    if command in [
        "previous video",
        "go to previous video",
        "play previous video",
    ]:
        return "previous_video", None

    # =========================================================
    # YOUTUBE MUTE
    # =========================================================

    if command in [
        "youtube mute",
        "mute youtube",
        "mute the video",
        "mute video",
    ]:
        return "youtube_mute", None


    # =========================================================
    # YOUTUBE UNMUTE
    # =========================================================

    if command in [
        "youtube unmute",
        "unmute youtube",
        "unmute the video",
        "unmute video", 
    ]:
        return "youtube_unmute", None


    # =========================================================
    # MEDIA SEEK
    # =========================================================

    if command in [
        "skip forward 10 seconds",
        "forward 10 seconds",
        "go forward 10 seconds",
    ]:
        return "seek_forward_10", None


    if command in [
        "go back 10 seconds",
        "skip back 10 seconds",
        "back 10 seconds",
    ]:
        return "seek_backward_10", None


    if command in [
        "skip forward 30 seconds",
        "forward 30 seconds",
        "go forward 30 seconds",
    ]:
        return "seek_forward_30", None


    if command in [
        "go back 30 seconds",
        "skip back 30 seconds",
        "back 30 seconds",
    ]:
        return "seek_backward_30", None



    # =========================================================
    # KEYBOARD CONTROL
    # =========================================================

    key_patterns = {
        "press enter": "enter",
        "press escape": "esc",
        "press tab": "tab",
        "press backspace": "backspace",
        "press delete": "delete",
        "press space": "space",
        "press the enter key": "enter",
        "press the escape key": "esc",
        "press the tab key": "tab",
    }

    for phrase, key in key_patterns.items():

        if command == phrase:

            return "press_key", key


    # =========================================================
    # NATURAL SHORTCUTS
    # =========================================================

    shortcut_map = {
        "copy": ["ctrl", "c"],
        "copy this": ["ctrl", "c"],

        "paste": ["ctrl", "v"],
        "paste this": ["ctrl", "v"],

        "cut": ["ctrl", "x"],
        "cut this": ["ctrl", "x"],

        "select all": ["ctrl", "a"],

        "undo": ["ctrl", "z"],
        "redo": ["ctrl", "y"],

        "save": ["ctrl", "s"],
        "save this": ["ctrl", "s"],

        "find": ["ctrl", "f"],
        "new tab": ["ctrl", "t"],
        "close tab": ["ctrl", "w"],
    }

    if command in shortcut_map:

        return "hotkey", shortcut_map[command]


    # =========================================================
    # NATURAL KEYBOARD HOTKEYS
    # =========================================================

    hotkey_patterns = [
        r"press\s+(.+?)\s+(?:and\s+)?press\s+(.+)",
        r"hold\s+(.+?)\s+and\s+press\s+(.+)",
        r"press\s+(.+?)\s+(.+)",
        r"(.+?)\s+(.+)",
    ]

    modifier_map = {
        "control": "ctrl",
        "ctrl": "ctrl",
        "shift": "shift",
        "alt": "alt",
        "windows": "win",
        "window": "win",
        "win": "win",
    }

    key_map = {
        "a": "a",
        "b": "b",
        "c": "c",
        "d": "d",
        "e": "e",
        "f": "f",
        "g": "g",
        "h": "h",
        "i": "i",
        "j": "j",
        "k": "k",
        "l": "l",
        "m": "m",
        "n": "n",
        "o": "o",
        "p": "p",
        "q": "q",
        "r": "r",
        "s": "s",
        "t": "t",
        "u": "u",
        "v": "v",
        "w": "w",
        "x": "x",
        "y": "y",
        "z": "z",

        "enter": "enter",
        "escape": "esc",
        "esc": "esc",
        "tab": "tab",
        "space": "space",
        "backspace": "backspace",
        "delete": "delete",
        "home": "home",
        "end": "end",
        "up": "up",
        "down": "down",
        "left": "left",
        "right": "right",
    }

    for pattern in hotkey_patterns:

        match = re.fullmatch(pattern, command)

        if not match:
            continue

        modifier_text = match.group(1).strip()
        key_text = match.group(2).strip()

        modifier = modifier_map.get(modifier_text)
        key = key_map.get(key_text)

        if modifier and key:

            return "hotkey", [modifier, key]




    # =========================================================
    # FIND / OPEN FOLDER
    # =========================================================

    match = re.fullmatch(
        r"(?:find|open)\s+(?:my\s+)?(.+?)\s+folder",
        command
    )

    if match:

        folder_name = match.group(1).strip()

        return "open_found_folder", folder_name



        # =========================================================
    # FIND / OPEN FILE
    # =========================================================

    match = re.fullmatch(
        r"(?:find|open)\s+(?:my\s+)?(.+)",
        command
    )

    if match:

        filename = match.group(1).strip()

        return "open_found_file", filename


    # =========================================================
    # VARIABLE MOUSE MOVEMENT
    # =========================================================

    match = re.fullmatch(
        r"move (?:the )?mouse (left|right|up|down)(?: (\d+))?(?: pixels?)?",
        command
    )

    if match:

        direction = match.group(1)

        distance = match.group(2)

        if distance:

            distance = int(distance)
        else:
            distance = 200

        return "move_mouse_variable", (direction, distance)


    # =========================================================
    # SMALL MOUSE MOVEMENT
    # =========================================================

    match = re.fullmatch(
        r"move (?:the )?mouse (a little )?(left|right|up|down)",
        command
    )

    if match:

        direction = match.group(2)

        return "move_mouse_variable", (direction, 75)



    # =========================================================
    # MOUSE CONTROL
    # =========================================================

    mouse_action_patterns = {
        "left click": "mouse_left_click",
        "left-click": "mouse_left_click",
        "click": "mouse_left_click",

        "right click": "mouse_right_click",
        "right-click": "mouse_right_click",

        "double click": "mouse_double_click",
        "double-click": "mouse_double_click",

        "middle click": "mouse_middle_click",
        "middle-click": "mouse_middle_click",
    }

    if command in mouse_action_patterns:

        return mouse_action_patterns[command], None


    # =========================================================
    # MOUSE MOVEMENT
    # =========================================================

    mouse_move_patterns = [
        (r"move (?:the )?mouse left", "left"),
        (r"move (?:the )?mouse right", "right"),
        (r"move (?:the )?mouse up", "up"),
        (r"move (?:the )?mouse down", "down"),
    ]

    for pattern, direction in mouse_move_patterns:

        if re.fullmatch(pattern, command):

            return "move_mouse", direction





    # =========================================================
    # FOCUS / SWITCH APPLICATION
    # =========================================================

    focus_patterns = [
        r"switch to (.+)",
        r"focus (?:on )?(.+)",
        r"bring (.+) to the front",
        r"bring (?:the )?(.+) to the front",
    ]

    for pattern in focus_patterns:

        match = re.fullmatch(pattern, command)

        if match:

            app_name = match.group(1).strip()

            return "focus_app", app_name


    # =========================================================
    # RUNNING APPS
    # =========================================================

    if command in [
        "what apps are running",
        "what applications are running",
        "show running apps",
        "show running applications",
        "what is running",
    ]:
        return "get_running_apps", None


    # =========================================================
    # CHECK APP
    # =========================================================

    match = re.fullmatch(
        r"(?:is|is the|check if)\s+(.+?)\s+(?:running|open)",
        command
    )

    if match:

        app_name = match.group(1).strip()

        return "check_app_running", app_name



    # =========================================================
    # CLIPBOARD
    # =========================================================

    if command in [
        "what is in my clipboard",
        "what's in my clipboard",
        "read my clipboard",
        "check my clipboard",
    ]:
        return "get_clipboard", None


    if command in [
        "clear my clipboard",
        "clear clipboard",
        "empty my clipboard",
        "empty clipboard",
    ]:
        return "clear_clipboard", None


    # =========================================================
    # TAKE SCREENSHOT
    # =========================================================

    if command in [
        "take a screenshot",
        "take screenshot",
        "capture the screen",
        "capture screen",
        "save a screenshot",
    ]:
        return "take_screenshot", None

    # =========================================================
    # OPEN LAST SCREENSHOT
    # =========================================================

    if command in [
        "open my last screenshot",
        "open the last screenshot",
        "show my last screenshot",
        "show the last screenshot",
    ]:
        return "open_last_screenshot", None



    
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
    # YOUTUBE SEARCH
    # =========================================================

    match = re.fullmatch(
        r"(?:search youtube for|youtube search for|search on youtube for)\s+(.+)",
        command
    )

    if match:
        
        query = match.group(1).strip()
        return "search_youtube", query


    # =========================================================
    # SKIP AD
    # =========================================================

    if (
        "skip ad" in command
        or "skip ads" in command
        or "skip the ad" in command
        or "skip advertisement" in command
    ):
        return "skip_ad", None

    # =========================================================
    # FULL SCREEN
    # =========================================================

    if (
        "full screen" in command
        or "fullscreen" in command
        or "go full screen" in command
    ):
        return "full_screen", None


    # =========================================================
    # EXIT FULL SCREEN
    # =========================================================

    if (
        "exit full screen" in command
        or "exit fullscreen" in command
        or "leave full screen" in command
        or "close full screen" in command
    ):
        return "exit_full_screen", None




    

    # =========================================================
    # GOOGLE SEARCH
    # =========================================================

    match = re.fullmatch(
        r"(?:search google for|google search for)\s+(.+)",
        command
    )

    if match:
        query = match.group(1).strip()
        return "search_google", query



    # =========================================================
    # BROWSER SEARCH
    # =========================================================

    match = re.match(
        r"(?:search for|search|look up|google)\s+(.+)",
        command
    )

    if match:

        query = match.group(1).strip()

        return "browser_search", query 


    # =========================================================
    # CLICK LINK BY NAME
    # =========================================================

    match = re.fullmatch(
        r"click\s+(.+)",
        command
    )

    if match:
        link_name = match.group(1).strip()

        return "click_link", link_name


    # =========================================================
    # FIND LINK AND CLICK
    # =========================================================

    match = re.fullmatch(
        r"find\s+(.+?)\s+(?:and\s+)?click(?:\s+it)?",
        command
    )

    if match:
        link_name = match.group(1).strip()

        return "click_link", link_name



    # =========================================================
    # SCROLL DOWN LITTLE
    # =========================================================

    scroll_down_little_patterns = [
        r"scroll down a little",
        r"scroll down little",
        r"scroll down slightly",
    ]

    for pattern in scroll_down_little_patterns:
        if re.fullmatch(pattern, command):
            return "scroll_down_little", None


    # =========================================================
    # SCROLL UP LITTLE
    # =========================================================

    scroll_up_little_patterns = [
        r"scroll up a little",
        r"scroll up little",
        r"scroll up slightly",
    ]

    for pattern in scroll_up_little_patterns:
        if re.fullmatch(pattern, command):
            return "scroll_up_little", None


    # =========================================================
    # SCROLL DOWN
    # =========================================================

    scroll_down_patterns = [
        r"scroll down",
        r"go down",
    ]

    for pattern in scroll_down_patterns:
        if re.fullmatch(pattern, command):
            return "scroll_down", None


    # =========================================================
    # SCROLL UP
    # =========================================================

    scroll_up_patterns = [
        r"scroll up",
        r"go up",
    ]

    for pattern in scroll_up_patterns:
        if re.fullmatch(pattern, command):
            return "scroll_up", None


    # =========================================================
    # GO FORWARD
    # =========================================================

    go_forward_patterns = [
        r"go forward",
        r"forward",
        r"next page",
        r"go to the next page",
    ]

    for pattern in go_forward_patterns:

        if re.fullmatch(pattern, command):
            return "go_forward", None

    # =========================================================
    # REFRESH PAGE
    # =========================================================

    refresh_page_patterns = [
        r"refresh",
        r"refresh page",
        r"refresh this page",
        r"reload",
        r"reload page",
        r"reload this page",
    ]

    for pattern in refresh_page_patterns:

        if re.fullmatch(pattern, command):
            return "refresh_page", None  

    # =========================================================
    # OPEN NEW TAB
    # =========================================================

    open_new_tab_patterns = [
        r"open new tab",
        r"new tab",
        r"create new tab",
    ]

    for pattern in open_new_tab_patterns:

        if re.fullmatch(pattern, command):
            return "open_new_tab", None



    # =========================================================
    # CLOSE CURRENT TAB
    # =========================================================

    close_current_tab_patterns = [
        r"close this tab",
        r"close current tab",
        r"close the tab",
        r"close tab",
    ]

    for pattern in close_current_tab_patterns:

        if re.fullmatch(pattern, command):
            return "close_current_tab", None



    # =========================================================
    # NEXT TAB
    # =========================================================

    next_tab_patterns = [
        r"next tab",
        r"switch to next tab",
        r"go to next tab",
    ]

    for pattern in next_tab_patterns:

        if re.fullmatch(pattern, command):
            return "next_tab", None


    # =========================================================
    # PREVIOUS TAB
    # =========================================================

    previous_tab_patterns = [
        r"previous tab",
        r"switch to previous tab",
        r"go to previous tab",
        r"last tab",
    ]

    for pattern in previous_tab_patterns:

        if re.fullmatch(pattern, command):
            return "previous_tab", None
    











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
    # NOTHING FOUND
    # =========================================================

    return None, None