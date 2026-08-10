from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

conversation_history = []


def ask_ai(prompt):
    global conversation_history

    # Build history BEFORE adding the current question
    recent_history = conversation_history[-10:]

    history = "\n".join(recent_history)

    full_prompt = f"""
You are Jarvis, my personal AI assistant.

Rules:
- Be friendly.
- Be concise.
- Answer naturally.
- If someone asks a programming question, explain clearly.
- Use the previous conversation to understand follow-up questions.
- Remember what the user was talking about.

Previous conversation:
{history}

User's latest message:
{prompt}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=full_prompt
    )

    answer = response.text

    # Save both sides of the conversation
    conversation_history.append(
        f"User: {prompt}"
    )

    conversation_history.append(
        f"Jarvis: {answer}"
    )

    return answer