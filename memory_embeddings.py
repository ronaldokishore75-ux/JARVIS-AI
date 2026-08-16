# =========================================================
# JARVIS V8.2.1 - SEMANTIC MEMORY EMBEDDINGS
# =========================================================

from embeddings import embed_text


def memory_to_text(memory):

    key = memory.get(
        "key",
        ""
    )

    value = memory.get(
        "value",
        ""
    )

    category = memory.get(
        "category",
        ""
    )

    return (
        f"{category}: "
        f"{key} = {value}"
    )


def embed_memory(memory):

    text = memory_to_text(
        memory
    )

    vector = embed_text(
        text
    )

    return {
        "memory_id": memory["id"],
        "text": text,
        "embedding": vector,
    }