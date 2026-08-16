# =========================================================
# JARVIS V8.1.9 - FLEXIBLE MEMORY + RAG ROUTER
# =========================================================

from memory_v8 import (
    load_memory,
    get_memory,
)

from memory_intent import (
    resolve_memory_key,
)


# =========================================================
# FIND MEMORY FOR QUESTION
# =========================================================

def find_memory_for_question(question):
    """
    Resolve a natural-language question to a structured
    memory key, then retrieve that memory.
    """

    key = resolve_memory_key(
        question
    )

    if not key:
        return None

    memory = load_memory()

    return get_memory(
        memory,
        key
    )


# =========================================================
# ROUTE QUESTION
# =========================================================

def route_question(
    question,
    rag_search_function
):
    """
    Routing order:

        1. Personal memory
        2. V4 RAG
        3. Nothing found
    """

    # -----------------------------------------------------
    # 1. MEMORY
    # -----------------------------------------------------

    memory_result = (
        find_memory_for_question(
            question
        )
    )

    if memory_result:

        return {
            "source": "memory",
            "memory": memory_result,
            "rag_results": None,
        }

    # -----------------------------------------------------
    # 2. V4 RAG
    # -----------------------------------------------------

    rag_results = rag_search_function(
        question,
        top_k=1
    )

    if rag_results:

        return {
            "source": "rag",
            "memory": None,
            "rag_results": rag_results,
        }

    # -----------------------------------------------------
    # 3. NOTHING FOUND
    # -----------------------------------------------------

    return {
        "source": None,
        "memory": None,
        "rag_results": None,
    }