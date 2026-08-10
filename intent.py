import re


def detect_intent(command):

    command = command.lower().strip()

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