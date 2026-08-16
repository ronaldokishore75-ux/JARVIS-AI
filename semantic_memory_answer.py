# =========================================================
# JARVIS V8.2.7 - SEMANTIC MEMORY ANSWERING
# =========================================================

from memory_v8 import load_memory

from memory_semantic_rag import (
    search_semantic_memory,
)

from memory_semantic_resolver import (
    resolve_memory_result,
)


# =========================================================
# ANSWER FROM SEMANTIC MEMORY
# =========================================================

def answer_from_semantic_memory(
    question,
    memory_vector_store,
    top_k=1
):
    """
    Search personal memory semantically, apply the existing
    confidence threshold, resolve the result back to the
    authoritative memory record, and build a concise answer.
    """

    if not question or not question.strip():
        return None

    # -----------------------------------------------------
    # Semantic search
    # -----------------------------------------------------

    results = search_semantic_memory(
        question,
        memory_vector_store,
        top_k=top_k,
    )

    if not results:
        return None

    # -----------------------------------------------------
    # Resolve authoritative memory record
    # -----------------------------------------------------

    resolved = resolve_memory_result(
        results[0]
    )

    if not resolved:
        return None

    # -----------------------------------------------------
    # Build answer
    # -----------------------------------------------------

    key = resolved.get(
        "key",
        ""
    )

    value = resolved.get(
        "value"
    )

    if value is None:
        return None

    readable_key = (
        key.replace(
            "_",
            " "
        )
    )

    return {
        "answer": (
            f"Your {readable_key} "
            f"is {value}."
        ),
        "memory": resolved,
    }