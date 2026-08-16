# =========================================================
# JARVIS V8.3 - MEMORY BRAIN INTEGRATION
# =========================================================

from memory_v8 import (
    load_memory,
)

from memory_semantic_rag import (
    build_memory_vector_store,
)

from hybrid_memory_answer import (
    answer_from_hybrid_memory,
)


# =========================================================
# BUILD MEMORY STATE
# =========================================================

def build_memory_state():

    memory_data = load_memory()

    vector_store = build_memory_vector_store(
        memory_data.get(
            "memories",
            []
        )
    )

    return (
        memory_data,
        vector_store,
    )


# =========================================================
# TRY MEMORY ANSWER
# =========================================================

def try_memory_answer(
    question
):

    memory_data, vector_store = (
        build_memory_state()
    )

    result = answer_from_hybrid_memory(
        question,
        vector_store,
        memory_data,
    )

    if not result:
        return None

    return result["answer"]