from datetime import datetime
from memory import load_memory, save_memory
from ai import ask_ai
from action import (
    open_google,
    open_youtube,
    open_notepad,
    open_calculator,
    open_chatgpt,
    open_gemini,
)

app_commands = {
    ("google", "browser", "search"): (open_google, "Opening Google."),
    ("youtube",): (open_youtube, "Opening YouTube."),
    ("notepad",): (open_notepad, "Opening Notepad."),
    ("calculator", "calc"): (open_calculator, "Opening Calculator."),
    ("chatgpt", "chat"): (open_chatgpt, "Opening ChatGPT."),
    ("gemini",): (open_gemini, "Opening Gemini."),
}


def jarvis_response(command):
    command = command.lower()
    memory = load_memory()

    if "hello" in command or "hi" in command:
        return "Hello! How can I help you?"

    if "your name" in command:
        return "I am Jarvis, your personal AI assistant."

    if "time" in command:
        return f"The current time is {datetime.now().strftime('%I:%M %p')}"

    if "date" in command:
        return f"Today is {datetime.now().strftime('%d %B %Y')}"

    if "how are you" in command:
        return "I am doing great. Thanks for asking."

    if 'my favorite color is' in command:
        color = command.replace('my favorite color is', '').strip()
        memory['favorite_color'] = color
        save_memory(memory)
        return f"Got it! I'll remember that your favorite color is {color}."

    if 'where do i live' in command:
        if 'location' in memory:
            return f"You live in {memory['location']}."
        else:
            return "I don't know where you live yet."
    
    if 'i live in' in command:
        city = command.replace('i live in', '').strip()
        memory['location'] = city
        save_memory(memory)
        return f"Got it! I'll remember that you live in {city}."

    if 'what is my favorite color' in command:
        if 'favorite_color' in memory:
            return f"Your favorite color is {memory['favorite_color']}."
        else:
            return "I don't know your favorite color yet."

    

    if "my name is" in command:
        name = command.replace("my name is", "").strip()
        memory["name"] = name
        save_memory(memory)
        return f"Nice to meet you, {name}. I'll remember your name."

    # Recall your name
    if "what is my name" in command:
        if "name" in memory:
            return f"Your name is {memory['name']}."
        else:
            return "I don't know your name yet."

    # Open applications

    for keywords, (action, message) in app_commands.items():
        if any(word in command for word in keywords):
            action()
            return message

    if "bye" in command:
        return "Goodbye! Have a great day!"

    if "thank you" in command or "thanks" in command:
        return "You're welcome!"

    if "joke" in command:
        return "Why don't scientists trust atoms? Because they make up everything!"

    return ask_ai(command)

