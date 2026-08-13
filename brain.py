from datetime import datetime
import re

from intent import detect_intent
from task_runner import request_task_cancel


from memory import load_memory, save_memory
from ai import ask_ai

from action import (
    open_google,
    search_google,
    open_youtube,
    search_youtube,
    open_notepad,
    open_calculator,
    open_chatgpt,
    open_gemini,
    open_jarvis_folder,
    open_jarvis_vscode,
    open_vscode,
    open_file_explorer,
    open_powershell,
    open_command_prompt,
    open_downloads,
    close_notepad,
    close_calculator,
    lock_computer,
    volume_up,
    volume_down,
    mute_volume,
    unmute_volume,
    get_cpu_usage,
    get_ram_usage,
    get_storage_usage,
    get_battery_level,
    set_volume,
    get_current_volume,
    start_timer,
    cancel_timer,
    get_timer_remaining,
    start_reminder,
    cancel_reminder,
    list_reminders,
    minimize_window,
    maximize_window,
    restore_window,
    close_window,
    show_desktop,
    sleep_computer,
    go_back,
    go_forward,
    refresh_page,
    open_new_tab,
    close_current_tab,
    next_tab,
    previous_tab,
    search_browser,
    search_google,
    search_youtube,
    scroll_down,
    scroll_up,
    scroll_down_little,
    scroll_up_little,
    click_link_by_name,
    skip_ad,
    full_screen,
    exit_full_screen,
    play_pause_media,
    next_video,
    previous_video,
    youtube_mute,
    youtube_unmute,
    seek_forward_10,
    seek_backward_10,
    seek_forward_30,
    seek_backward_30,
    take_screenshot,
    open_last_screenshot,
    get_clipboard,
    clear_clipboard,
    get_running_apps,
    is_app_running,
    focus_app,
    press_key,
    hotkey,
    open_found_file,
    open_found_folder,
    mouse_left_click,
    mouse_right_click,
    mouse_double_click,
    mouse_middle_click,
    move_mouse_left,
    move_mouse_right,
    move_mouse_up,
    move_mouse_down,






)

pending_action = None



def task_progress(event, step, total, description):

    if event == "step_started":

        print(
            f"V5 PROGRESS: Step {step}/{total}: "
            f"{description}"
        )

    elif event == "step_completed":

        print(
            f"V5 PROGRESS: Completed "
            f"{step}/{total}: {description}"
        )

    elif event == "completed":

        print(
            "V5 PROGRESS: Task completed."
        )

    elif event == "cancelled":

        print(
            "V5 PROGRESS: Task cancelled."
        )

    elif event == "failed":

        print(
            f"V5 PROGRESS: Task failed at "
            f"step {step}/{total}."
        )



def _rebuild_step_command(action, value):

    if action == "open_youtube":
        return "open youtube"

    if action == "search_youtube":
        return (
            f"search youtube for {value}"
        )

    if action == "scroll_down":
        return "scroll down"

    if action == "click_link":
        return f"click {value}"

    return action

def jarvis_response(command, _task_step=False):


    global pending_action
    
    command = command.lower().strip()

    # =========================================================
    # CANCEL V5 TASK
    # =========================================================

    cancel_intent, cancel_value = detect_intent(command)

    if cancel_intent == "cancel_task":

        from task_runner import request_task_cancel

        request_task_cancel()

        return "Cancelling the current task."



    # =========================================================
    # V5 LIVE TASK ENGINE
    # =========================================================

    if not _task_step:

        
        from task_manager import start_task

        # Use planner to decide whether this is a multi-step task
        from planner import create_plan

        plan = create_plan(command)

        if len(plan.steps) > 1:

            started = start_task(
                command,
                lambda action, value:
                    jarvis_response(
                        _rebuild_step_command(
                            action,
                            value
                        ),
                        _task_step=True
                    ),
                task_progress
            )


            if started:

                return "Starting the task."

            return (
                "A task is already running. "
                "Say stop task to cancel it."
            )



    memory = load_memory()

    # =========================================================
    # CONFIRMATION SYSTEM
    # =========================================================

    if pending_action is not None:

        if command in [
            "yes",
            "yeah",
            "yep",
            "sure",
            "okay",
            "ok",
            "do it",
        ]:

            action = pending_action

            pending_action = None

            if action == "close_notepad":
                close_notepad()
                return "Closing Notepad."

            elif action == "close_calculator":
                close_calculator()
                return "Closing Calculator."
            
            elif action=="close_window":
                close_window()
                return"closing the window"

            elif action=="sleep_computer":

                sleep_computer()

                return"putting the computer to sleep"
            

        elif command in [
            "no",
            "nope",
            "cancel",
            "don't",
            "dont",
            "never mind",
            "never",
        ]:

            pending_action = None

            return "Okay, I'll leave it open."

        else:

            return (
                "I didn't get a yes or no. "
                "Should I do it?"
            )

    # =========================================================
    # LOCAL INTENT SYSTEM
    # =========================================================

    intent, value = detect_intent(command)

    print(f"DEBUG: intent= {intent},value= {value}")

    # =========================================================
    # OPEN GOOGLE
    # =========================================================

    if intent == "open_google":

        open_google()

        return "Opening Google."

    # =========================================================
    # OPEN YOUTUBE
    # =========================================================

    elif intent == "open_youtube":

        open_youtube()

        return "Opening YouTube."


    elif intent == "search_google":

        search_google(value)

        return f"Searching Google for {value}."


    elif intent == "search_youtube":

        search_youtube(value)

        return f"Searching YouTube for {value}."

    elif intent == "task_status":


        from task_state import task_state

        state = task_state.get_state()

        if state["status"] == "IDLE":

            return "There is no active task."

        if state["status"] == "RUNNING":

            return (
                f"Task is running. "
                f"Step {state['current_step']} "
                f"of {state['total_steps']}. "
                f"Current action: "
                f"{state['current_action']}."
            )

        if state["status"] == "COMPLETED":

            return (
                f"The task is completed. "
                f"It finished all "
                f"{state['total_steps']} steps."
            )

        if state["status"] == "CANCELLED":

            return (
                f"The task was cancelled at "
                f"step {state['current_step']} "
                f"of {state['total_steps']}."
            )

        if state["status"] == "FAILED":

            return (
                f"The task failed at "
                f"step {state['current_step']} "
                f"of {state['total_steps']}. "
                f"Reason: {state['error']}."
            )

        return (
            f"Task status is "
            f"{state['status']}."
        )


    elif intent == "browser_search":

        search_browser(value)

        return f"Searching for {value}."


    elif intent == "play_pause_media":

        play_pause_media()

        return "Toggling play and pause."


    elif intent == "next_video":

        next_video()

        return "Playing the next video."

    elif intent == "previous_video":

        previous_video()

        return "Playing the previous video."

    elif intent == "youtube_mute":

        youtube_mute()

        return "Muting YouTube."

    elif intent == "youtube_unmute":

        youtube_unmute()

        return "Unmuting YouTube."

    elif intent == "seek_forward_10":

        seek_forward_10()

        return "Skipping forward 10 seconds."


    elif intent == "seek_backward_10":

        seek_backward_10()

        return "Going back 10 seconds."


    elif intent == "seek_forward_30":

        seek_forward_30()

        return "Skipping forward 30 seconds."


    elif intent == "seek_backward_30":

        seek_backward_30()

        return "Going back 30 seconds."




    # =========================================================
    # VARIABLE MOUSE MOVEMENT
    # =========================================================

    elif intent == "move_mouse_variable":

        direction, distance = value

        if direction == "left":

            move_mouse_left(distance)

            return f"Moving the mouse left {distance} pixels."

        elif direction == "right":

            move_mouse_right(distance)

            return f"Moving the mouse right {distance} pixels."

        elif direction == "up":

            move_mouse_up(distance)

            return f"Moving the mouse up {distance} pixels."

        elif direction == "down":

            move_mouse_down(distance)

            return f"Moving the mouse down {distance} pixels."

    # =========================================================
    # MOUSE MOVEMENT
    # =========================================================

    elif intent == "move_mouse":

        if value == "left":

            move_mouse_left()

            return "Moving the mouse left."

        elif value == "right":

            move_mouse_right()

            return "Moving the mouse right."

        elif value == "up":

            move_mouse_up()

            return "Moving the mouse up."

        elif value == "down":

            move_mouse_down()

            return "Moving the mouse down."

    # =========================================================
    # MOUSE CONTROL
    # =========================================================

    elif intent == "mouse_left_click":

        mouse_left_click()

        return "Left clicking."


    elif intent == "mouse_right_click":

        mouse_right_click()

        return "Right clicking."


    elif intent == "mouse_double_click":

        mouse_double_click()

        return "Double clicking."


    elif intent == "mouse_middle_click":

        mouse_middle_click()

        return "Middle clicking."



    #===============================================
    # HOTKEYS
    #==========================================


    elif intent == "press_key":

        press_key(value)

        return f"Pressing {value}."

    elif intent == "hotkey":

        hotkey(value)

        return f"Pressing {' + '.join(value)}."


    #================================================
    # oprn file  downlaods
    #==============================================


    elif intent == "open_found_file":

        if open_found_file(value):

            return f"Opening {value}."

        return f"I couldn't find {value}."

    elif intent == "open_found_folder":

        if open_found_folder(value):

            return f"Opening {value} folder."

        return f"I couldn't find the {value} folder."




    # #=================================================
    # FOCUS APP ===============
    #======================================================


    elif intent == "focus_app":

        if focus_app(value):

            return f"Switching to {value}."

        return f"I couldn't find {value} running."


    #=====================================================
    # RUNNING APPS
    #===================================================

    elif intent == "get_running_apps":

        apps = get_running_apps()

        if isinstance(apps, str):
            return apps

    # Don't make JARVIS speak hundreds of processes.
    # Show the useful application/process names in the terminal.
        print("Running applications:")


        for app in apps:
            print(app)

        return f"I found {len(apps)} running processes. I've listed them in the console."


    elif intent == "check_app_running":

        if is_app_running(value):

            return f"Yes, {value} is running."

        return f"No, {value} is not running."




    #============================================================
    # CLIPBOARD
    #===========================================

    elif intent == "get_clipboard":

        return get_clipboard()

    elif intent == "clear_clipboard":

        if clear_clipboard():
            return "Clipboard cleared."

        return "I couldn't clear the clipboard."


    #=============================================================
    #SCREENSHOT
    #======================================================


    elif intent == "take_screenshot":

        filepath = take_screenshot()

        return "Screenshot saved successfully."

    elif intent == "open_last_screenshot":

        if open_last_screenshot():
            return "Opening your last screenshot."

        return "I couldn't find any screenshots."





     # =========================================================
    #    SCROLL DOWN LITTLE
    # =========================================================

    elif intent == "scroll_down_little":

        scroll_down_little()

        return "Scrolling down a little."


# =========================================================
# SCROLL UP LITTLE
# =========================================================

    elif intent == "scroll_up_little":

        scroll_up_little()

        return "Scrolling up a little."


# =========================================================
# SCROLL DOWN
# =========================================================

    elif intent == "scroll_down":

        scroll_down()

        return "Scrolling down."


# =========================================================
# SCROLL UP
# =========================================================

    elif intent == "scroll_up":

        scroll_up()

        return "Scrolling up."

    # =========================================================
    # CLICK LINK
    # =========================================================

    elif intent == "click_link":

        success = click_link_by_name(value)

        if success:
            return f"Clicking {value}."

        return f"I couldn't find {value}."

    elif intent == "skip_ad":

        if skip_ad():
        
            return "Skipping the ad."

        return "I couldn't find a skip button."

    elif intent == "full_screen":

        full_screen()

        return "Entering full screen."


    elif intent == "exit_full_screen":

        exit_full_screen()

        return "Exiting full screen."


    elif intent == "go_back":

        go_back()

        return "Going back."

    elif intent == "go_forward":

        go_forward()

        return "Going forward."

    elif intent == "refresh_page":

        refresh_page()

        return "Refreshing the page."

    elif intent == "open_new_tab":

        open_new_tab()

        return "Opening a new tab."
    

    elif intent == "close_current_tab":

        close_current_tab()

        return "Closing this tab."

    elif intent == "next_tab":

        next_tab()

        return "Switching to the next tab."

    elif intent == "previous_tab":

        previous_tab()

        return "Switching to the previous tab."




    # =========================================================
    # WINDOW CONTROL
    # =========================================================

    elif intent == "minimize_window":

        minimize_window()
        return "Minimizing the window."


    elif intent == "maximize_window":

        maximize_window()
        return "Maximizing the window."


    elif intent == "restore_window":

        restore_window()
        return "Restoring the window."


    elif intent == "yes":

        if pending_action=="close_window":

            close_window()

            pending_action=None

            return "closing the window"

    elif intent=="no":
        if pending_action=="close_window":

            pending_action=None

            return "okay ,I wont close the window"


    elif intent == "show_desktop":

        show_desktop()

        return "Showing the desktop."

    

    elif intent == "sleep_computer":

        pending_action = "sleep_computer"

        return "Are you sure you want to put the computer to sleep?"

    

    # =========================================================
    # LOCK COMPUTER
    # =========================================================

    elif intent == "lock_computer":

        lock_computer()

        return "Locking your computer."

    #==========================================================
    #COMPUTER FUNCTION
    #===========================================================

    elif intent == "cpu_usage":

        return get_cpu_usage()


    elif intent == "ram_usage":

        return get_ram_usage()


    elif intent == "storage_usage":

        return get_storage_usage()


    elif intent == "battery_level":

        return get_battery_level()



    # =========================================================
    # VOLUME UP
    # =========================================================

    elif intent == "volume_up":

        volume_up()

        return "Increasing volume."

    # =========================================================
    # VOLUME DOWN
    # =========================================================

    elif intent == "volume_down":

        volume_down()

        return "Decreasing volume."

    # =========================================================
    # MUTE
    # =========================================================

    elif intent == "mute_volume":

        mute_volume()

        return "Muting volume."

    # =========================================================
    # UNMUTE
    # =========================================================

    elif intent == "unmute_volume":

        unmute_volume()

        return "Unmuting volume."
    #============================================================
    # volume set
    #============================================================

    elif intent == "set_volume":

        return set_volume(value)


    elif intent == "get_current_volume":

        return get_current_volume()

    # =========================================================
    # OPEN NOTEPAD
    # =========================================================

    elif intent == "open_notepad":

        open_notepad()

        return "Opening Notepad."

    # =========================================================
    # OPEN CALCULATOR
    # =========================================================

    elif intent == "open_calculator":

        open_calculator()

        return "Opening Calculator."

    # =========================================================
    # OPEN VS CODE
    # =========================================================

    elif intent == "open_vscode":

        open_vscode()

        return "Opening Visual Studio Code."

    # =========================================================
    # OPEN FILE EXPLORER
    # =========================================================

    elif intent == "open_file_explorer":

        open_file_explorer()

        return "Opening File Explorer."

    # =========================================================
    # OPEN DOWNLOADS
    # =========================================================

    elif intent == "open_downloads":

        open_downloads()

        return "Opening your Downloads folder."

    # =========================================================
    # OPEN POWERSHELL
    # =========================================================

    elif intent == "open_powershell":

        open_powershell()

        return "Opening PowerShell."

    # =========================================================
    # OPEN COMMAND PROMPT
    # =========================================================

    elif intent == "open_command_prompt":

        open_command_prompt()

        return "Opening Command Prompt."

    # =========================================================
    # OPEN JARVIS FOLDER
    # =========================================================

    elif intent == "open_jarvis_folder":

        open_jarvis_folder()

        return "Opening your Jarvis project folder."

    # =========================================================
    # OPEN JARVIS IN VS CODE
    # =========================================================

    elif intent == "open_jarvis_vscode":

        open_jarvis_vscode()

        return "Opening your Jarvis project in Visual Studio Code."

    #=============================================================
    #timer
    #=============================================================


    elif intent == "set_timer":
        start_timer(value)


        if value < 60:

            return f"Timer set for {value} seconds."

        if value < 3600:

            minutes = value // 60

            if minutes == 1:
                return "Timer set for 1 minute."

            return f"Timer set for {minutes} minutes."

        hours = value // 3600

        if hours == 1:
            return "Timer set for 1 hour."

        return f"Timer set for {hours} hours."
    

    elif intent == "cancel_timer":

        return cancel_timer()
    

    elif intent == "timer_remaining":

        remaining = get_timer_remaining()

        if remaining is None:
            return "You don't have an active timer."

        if remaining < 60:
            return f"You have {remaining} seconds remaining."
        minutes = remaining // 60
        seconds = remaining % 60

        if seconds == 0:

            return f"You have {minutes} minutes remaining."
        return (
            f"You have {minutes} minutes "
            f"and {seconds} seconds remaining."
            )


    elif intent == "set_reminder":

        seconds, message = value

        start_reminder(seconds, message)


        if seconds < 60:
            return f"Reminder set for {seconds} seconds."

        if seconds < 3600:

            minutes = seconds // 60

            if message == "Your reminder":

                return f"Reminder set for {minutes} minutes."
            return f"I'll remind you in {minutes} minutes to {message}."

        hours = seconds // 3600

        if message == "Your reminder":

            return f"Reminder set for {hours} hours."
        return f"I'll remind you in {hours} hours to {message}."
    

    elif intent == "cancel_reminder":

        return cancel_reminder()


    elif intent == "list_reminders":

        return list_reminders()
    # =========================================================
    # SEARCH GOOGLE
    # =========================================================

    elif intent == "search_google":

        search_google(value)

        return f"Searching Google for {value}."

    # =========================================================
    # SEARCH YOUTUBE
    # =========================================================

    elif intent == "search_youtube":

        search_youtube(value)

        return f"Searching YouTube for {value}."

    # =========================================================
    # CLOSE NOTEPAD
    # =========================================================

    elif intent == "close_notepad":

        pending_action = "close_notepad"

        return "Are you sure you want to close Notepad?"

    # =========================================================
    # CLOSE CALCULATOR
    # =========================================================

    elif intent == "close_calculator":


        pending_action = "close_calculator"

        return "Are you sure you want to close Calculator?"

    # =========================================================
    # DIRECT CLOSE COMMANDS
    #
    # Safety net in case intent.py doesn't recognize
    # the exact wording.
    # =========================================================

    if command in [
        "close notepad",
        "close the notepad",
        "exit notepad",
        "exit the notepad",
        "quit notepad",
        "quit the notepad",
    ]:

        close_notepad()

        return "Closing Notepad."

    if command in [
        "close calculator",
        "close the calculator",
        "close calc",
        "exit calculator",
        "exit the calculator",
        "quit calculator",
        "quit the calculator",
    ]:

        close_calculator()

        return "Closing Calculator."

    # =========================================================
    # DIRECT OPEN COMMANDS
    #
    # Safety net for common Windows applications.
    # =========================================================

    if command in [
        "open notepad",
        "open the notepad",
        "launch notepad",
        "launch the notepad",
        "start notepad",
        "start the notepad",
        "open my notepad",
    ]:

        open_notepad()

        return "Opening Notepad."

    if command in [
        "open calculator",
        "open the calculator",
        "open calc",
        "launch calculator",
        "launch the calculator",
        "start calculator",
        "start the calculator",
        "open my calculator",
    ]:

        open_calculator()

        return "Opening Calculator."

    # =========================================================
    # GREETINGS
    # =========================================================

    if command in ["hello", "hi", "hey"]:

        return "Hello! How can I help you?"

    # =========================================================
    # JARVIS INFORMATION
    # =========================================================

    if "your name" in command:

        return "I am Jarvis, your personal AI assistant."


  

    # =========================================================
    # CURRENT TIME
    # =========================================================

    time_patterns = [

        r"what time is it",
        r"what is the time",
        r"what's the time",
        r"tell me the time",
        r"what is the current time",
        r"what's the current time",
        r"current time",
        r"time now",
        ]

    if any(re.fullmatch(pattern, command) for pattern in time_patterns):

        return f"The current time is {datetime.now().strftime('%I:%M %p')}"
    # =========================================================
    # DATE
    # =========================================================

    if "date" in command:

        return (
            f"Today is "
            f"{datetime.now().strftime('%d %B %Y')}"
        )

    # =========================================================
    # HOW ARE YOU
    # =========================================================

    if "how are you" in command:

        return "I am doing great. Thanks for asking."

    # =========================================================
    # FAVORITE COLOR
    # =========================================================

    if "my favorite color is" in command:

        color = command.replace(
            "my favorite color is",
            "",
            1
        ).strip()

        memory["favorite_color"] = color

        save_memory(memory)

        return (
            f"Got it! I'll remember that "
            f"your favorite color is {color}."
        )

    if "what is my favorite color" in command:

        if "favorite_color" in memory:

            return (
                f"Your favorite color is "
                f"{memory['favorite_color']}."
            )

        return "I don't know your favorite color yet."

    # =========================================================
    # LOCATION
    # =========================================================

    if "i live in" in command:

        city = command.replace(
            "i live in",
            "",
            1
        ).strip()

        memory["location"] = city

        save_memory(memory)

        return (
            f"Got it! I'll remember "
            f"that you live in {city}."
        )

    if "where do i live" in command:

        if "location" in memory:

            return (
                f"You live in "
                f"{memory['location']}."
            )

        return "I don't know where you live yet."

    # =========================================================
    # NAME
    # =========================================================

    if "my name is" in command:

        name = command.replace(
            "my name is",
            "",
            1
        ).strip()

        memory["name"] = name

        save_memory(memory)

        return (
            f"Nice to meet you, {name}. "
            f"I'll remember your name."
        )

    if "what is my name" in command:

        if "name" in memory:

            return (
                f"Your name is "
                f"{memory['name']}."
            )

        return "I don't know your name yet."

    # =========================================================
    # GOOGLE SEARCH
    # =========================================================

    google_match = re.search(
        r"(?:open\s+)?google"
        r"(?:\s+and)?"
        r"\s+search\s+(?:for\s+)?(.+)",
        command
    )

    if google_match:

        query = google_match.group(1).strip()

        query = query.rstrip("-").strip()

        if query:

            search_google(query)

            return (
                f"Searching Google for {query}."
            )

    # =========================================================
    # SEARCH ON GOOGLE
    # =========================================================

    google_match = re.search(
        r"(?:search|find)\s+"
        r"(?:for\s+)?(.+?)\s+on\s+google$",
        command
    )

    if google_match:

        query = google_match.group(1).strip()

        if query:

            search_google(query)

            return (
                f"Searching Google for {query}."
            )

    # =========================================================
    # YOUTUBE SEARCH
    # =========================================================

    youtube_match = re.search(
        r"(?:open\s+)?youtube"
        r"(?:\s+and|\s+on)?"
        r"\s+search\s+(?:for\s+)?(.+)",
        command
    )

    if youtube_match:

        query = youtube_match.group(1).strip()

        query = query.rstrip("-").strip()

        if query:

            search_youtube(query)

            return (
                f"Searching YouTube for {query}."
            )

    # =========================================================
    # SEARCH ON YOUTUBE
    # =========================================================

    youtube_match = re.search(
        r"(?:search|find)\s+"
        r"(?:for\s+)?(.+?)\s+on\s+youtube$",
        command
    )

    if youtube_match:

        query = youtube_match.group(1).strip()

        if query:

            search_youtube(query)

            return (
                f"Searching YouTube for {query}."
            )

        

    # =========================================================
    # SIMPLE SEARCH
    # =========================================================

    if command.startswith("search "):

        query = command.replace(
            "search ",
            "",
            1
        ).strip()

        if query and "youtube" not in query:

            search_google(query)

            return (
                f"Searching Google for {query}."
            )

    # =========================================================
    # JARVIS FOLDER
    # =========================================================

    if (
        "open jarvis folder" in command
        or "open my jarvis folder" in command
        or "open my project folder" in command
    ):

        open_jarvis_folder()

        return (
            "Opening your Jarvis project folder."
        )

    # =========================================================
    # JARVIS IN VS CODE
    # =========================================================

    if (
        "open jarvis in vscode" in command
        or "open jarvis in vs code" in command
        or "open jarvis project" in command
    ):

        open_jarvis_vscode()

        return (
            "Opening your Jarvis project "
            "in Visual Studio Code."
        )

    # =========================================================
    # WINDOWS CONTROLS
    # =========================================================

    if command in [
        "open vscode",
        "open vs code",
        "open visual studio code",
    ]:

        open_vscode()

        return "Opening Visual Studio Code."

    if command in [
        "open file explorer",
        "open explorer",
    ]:

        open_file_explorer()

        return "Opening File Explorer."

    if command in [
        "open powershell",
    ]:

        open_powershell()

        return "Opening PowerShell."

    if command in [
        "open command prompt",
        "open cmd",
    ]:

        open_command_prompt()

        return "Opening Command Prompt."

    if command in [
        "open downloads",
        "open my downloads",
    ]:

        open_downloads()

        return "Opening your Downloads folder."

    # =========================================================
    # CHATGPT
    # =========================================================

    if command in [
        "open chatgpt",
        "open chat gpt",
        "launch chatgpt",
        "start chatgpt",
    ]:

        open_chatgpt()

        return "Opening ChatGPT."

    # =========================================================
    # GEMINI
    # =========================================================

    if command in [
        "open gemini",
        "launch gemini",
        "start gemini",
    ]:

        open_gemini()

        return "Opening Gemini."

    # =========================================================
    # GOODBYE
    # =========================================================

    if "bye" in command:

        return "Goodbye! Have a great day!"

    # =========================================================
    # THANK YOU
    # =========================================================

    if (
        "thank you" in command
        or "thanks" in command
    ):

        return "You're welcome!"

    # =========================================================
    # JOKE
    # =========================================================

    if "joke" in command:

        return (
            "Why don't scientists trust atoms? "
            "Because they make up everything!"
        )

    # =========================================================
    # GEMINI FALLBACK
    #
    # Only unknown commands/questions reach Gemini.
    # =========================================================

    return ask_ai(command)