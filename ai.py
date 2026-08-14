from google import genai
from config import GEMINI_API_KEY
import time

client = genai.Client(
    api_key=GEMINI_API_KEY
)

conversation_history = []


def ask_ai(prompt):

    global conversation_history

    recent_history = conversation_history[-10:]

    history = "\n".join(
        recent_history
    )

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

    max_attempts = 3

    for attempt in range(
        max_attempts
    ):

        try:

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=full_prompt
            )

            answer = response.text

            conversation_history.append(
                f"User: {prompt}"
            )

            conversation_history.append(
                f"Jarvis: {answer}"
            )

            return answer

        except Exception as error:

            print(
                f"AI ERROR "
                f"(attempt {attempt + 1}/{max_attempts}): "
                f"{error}"
            )

            if attempt < max_attempts - 1:

                wait_time = 2 ** attempt

                print(
                    f"Retrying in "
                    f"{wait_time} seconds..."
                )

                time.sleep(
                    wait_time
                )

    return (
        "Gemini is temporarily unavailable. "
        "Please try again in a moment."
    )