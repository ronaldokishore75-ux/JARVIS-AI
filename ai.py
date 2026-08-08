import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-3.5-flash")


def ask_ai(prompt):
    response = model.generate_content(
        f"""
You are Jarvis, my personal AI assistant.

Rules:
- Be friendly.
- Be concise.
- Answer naturally.
- If someone asks a programming question, explain clearly.

User: {prompt}
"""
    )

    return response.text