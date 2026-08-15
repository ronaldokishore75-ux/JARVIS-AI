# =========================================================
# JARVIS V6.3 - LOCAL LLM ADAPTER
# =========================================================

import re
import requests


OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"
MODEL_NAME = "qwen3:4b-instruct"



# =========================================================
# RAW LOCAL MODEL RESPONSE
# =========================================================

def ask_local_raw(prompt):

    if not prompt or not prompt.strip():
        raise ValueError(
            "Prompt cannot be empty."
        )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are JARVIS. "
                    "Follow the user's instructions exactly."
                ),
            },
            {
                "role": "user",
                "content": prompt.strip(),
            },
        ],
        "stream": False,
        "think": True,
        "options": {
            "temperature": 0.1,
            "num_predict": 400,
            "num_ctx": 2048,
        },
    }

    response = requests.post(
        OLLAMA_CHAT_URL,
        json=payload,
        timeout=240,
    )

    response.raise_for_status()

    data = response.json()

    message = data.get(
        "message",
        {}
    )

    content = message.get(
        "content",
        ""
    )

    thinking = message.get(
        "thinking",
        ""
    )

    # Prefer final content.
    if content:
        return content.strip()

    # Qwen may put the useful JSON at the end of
    # the thinking field.
    if thinking:
        return thinking.strip()

    return data.get(
        "response",
        ""
    ).strip()




def _extract_final_answer(text):
    """
    Extract the useful final answer from Qwen's thinking text.
    """

    if not text:
        return ""

    text = text.strip()

    # -----------------------------------------------------
    # Remove <think> blocks if present
    # -----------------------------------------------------

    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.IGNORECASE | re.DOTALL
    ).strip()

    # -----------------------------------------------------
    # Try common explicit answer markers
    # -----------------------------------------------------

    patterns = [
        r"(?is)final answer\s*:\s*(.+)$",
        r"(?is)answer\s*:\s*(.+)$",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:
            return match.group(1).strip()

    # -----------------------------------------------------
    # Look for a concise final sentence near the end
    # -----------------------------------------------------

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # Prefer lines that look like actual answer text.
    candidates = []

    for line in lines:

        lower = line.lower()

        if any(
            marker in lower
            for marker in [
                "we are given",
                "the question is",
                "we must",
                "from the context",
                "i need to",
                "i should",
                "let me",
                "the user wants",
                "the user says",
                "steps:",
                "option 1:",
                "option 2:",
                "important:",
            ]
        ):
            continue

        candidates.append(line)

    if candidates:
        return candidates[-1]

    return lines[-1] if lines else ""


def ask_local(prompt):

    if not prompt or not prompt.strip():

        raise ValueError(
            "Prompt cannot be empty."
        )

    payload = {
        "model": MODEL_NAME,

        "messages": [
            {
                "role": "system",
                "content": (
                    "You are JARVIS, a personal AI assistant. "
                    "Return a concise final answer. "
                    "Do not reveal internal reasoning."
                ),
            },

            {
                "role": "user",
                "content": prompt.strip(),
            },
        ],

        "stream": False,

        "think": True,

        "options": {
            "temperature": 0.2,
            "num_predict": 400,
            "num_ctx": 2048,
        },
    }

    try:

        response = requests.post(
            OLLAMA_CHAT_URL,
            json=payload,
            timeout=240,
        )

        response.raise_for_status()

    except requests.exceptions.Timeout as error:

        raise RuntimeError(
            "Ollama timed out while generating "
            "the response."
        ) from error

    data = response.json()

    message = data.get(
        "message",
        {}
    )

    # -----------------------------------------------------
    # Preferred final response
    # -----------------------------------------------------

    answer = message.get(
        "content",
        ""
    )

    # -----------------------------------------------------
    # Qwen3 may put the answer inside thinking when the
    # final content field is empty.
    # -----------------------------------------------------

    if not answer:

        thinking = message.get(
            "thinking",
            ""
        )

        answer = _extract_final_answer(
            thinking
        )

    # -----------------------------------------------------
    # Fallback to generate-style response if present
    # -----------------------------------------------------

    if not answer:

        answer = data.get(
            "response",
            ""
        )

    answer = _extract_final_answer(
        answer
    )

    if not answer:

        raise RuntimeError(
            f"Ollama returned no usable answer: {data}"
        )

    return answer.strip()