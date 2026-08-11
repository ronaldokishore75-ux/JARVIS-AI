from datetime import datetime
import re

from intent import detect_intent

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
)

pending_action = None

def jarvis_response(command):

    global pending_action
    
    command = command.lower().strip()

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
    # TIME
    # =========================================================

    if "time" in command:

        return (
            f"The current time is "
            f"{datetime.now().strftime('%I:%M %p')}"
        )

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