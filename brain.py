from datetime import datetime

def jarvis_response(command):
    command = command.lower()

    if "hello" in command or "hi" in command:
        return "Hello! How can I help you?"

    elif "your name" in command:
        return "I am Jarvis, your personal AI assistant."

    elif "time" in command:
        return f"The current time is {datetime.now().strftime('%I:%M %p')}"

    elif "date" in command:
        return f"Today is {datetime.now().strftime('%d %B %Y')}"

    elif "how are you" in command:
        return "I am doing great. Thanks for asking."

    else:
        return f"You said: {command}. I don't know how to answer that yet."