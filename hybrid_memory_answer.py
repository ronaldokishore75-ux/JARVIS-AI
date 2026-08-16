# =========================================================
# JARVIS V8.2.9 - HYBRID MEMORY ANSWERING
# =========================================================

from memory_hybrid_retrieval import (
    retrieve_memory,
)


def answer_from_hybrid_memory(
    question,
    memory_vector_store,
    memory_data,
):
    """
    Retrieve a memory using the hybrid structured +
    semantic memory system and generate a direct answer.
    """

    if not question or not question.strip():
        return None

    result = retrieve_memory(
        question,
        memory_vector_store,
        memory_data,
    )

    if not result:
        return None

    key = result.get(
        "key",
        ""
    )

    value = result.get(
        "value"
    )

    if value is None:
        return None

    readable_key = key.replace(
        "_",
        " "
    )

    # -----------------------------------------------------
    # Natural answer templates
    # -----------------------------------------------------

    if key == "name":

        answer = (
            f"Your name is {value}."
        )

    elif key == "favorite_color":

        answer = (
            f"Your favorite color is {value}."
        )

    elif key == "location":

        answer = (
            f"You live in {value}."
        )

    else:

        answer = (
            f"Your {readable_key} is {value}."
        )

    return {
        "answer": answer,
        "memory": result,
    }