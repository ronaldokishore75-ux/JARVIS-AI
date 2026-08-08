from datetime import datetime
from action import open_google, open_youtube, open_notepad, open_calculator, open_chatgpt, open_gemini

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

    elif "open google" in command:
        open_google()
        return "Opening Google."
    
    elif "open youtube" in command:
        open_youtube()
        return "Opening YouTube."
    
    elif "open notepad" in command:
        open_notepad()
        return "Opening Notepad."

    elif "open calculator" in command:
        open_calculator()
        return "Opening Calculator."

    elif "open chatgpt" in command:
        open_chatgpt()
        return "Opening ChatGPT."

    elif "open gemini" in command:
        open_gemini()
        return "Opening Gemini."

    elif "bye" in command:
        return "Goodbye! Have a great day!"

    elif "thank you" in command or "thanks" in command:
        return "You're welcome!"

    elif "joke" in command:
        return "Why don't scientists trust atoms? Because they make up everything!" 


    else:
        return f"You said: {command}. I don't know how to answer that yet."
    

    

    