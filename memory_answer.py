# =========================================================
# JARVIS V8.1.6 - MEMORY-AWARE ANSWERING
# =========================================================

from memory_v8 import (
    load_memory,
    get_memory,
)


# =========================================================
# ANSWER FROM MEMORY
# =========================================================

def answer_from_memory(
    key
):
    """
    Retrieve one structured memory by key.

    Returns:
        dict | None
    """

    memory = load_memory()

    result = get_memory(
        memory,
        key
    )

    return result


# =========================================================
# BUILD A SIMPLE ANSWER
# =========================================================

def format_memory_answer(
    key
):
    """
    Turn a stored memory into a simple JARVIS answer.
    """

    result = answer_from_memory(
        key
    )

    if not result:

        return None

    value = result.get(
        "value"
    )

    if value is None:

        return None

    return (
        f"Your {key.replace('_', ' ')} "
        f"is {value}."
    )