# =========================================================
# JARVIS V8.2.8 - HYBRID MEMORY RETRIEVAL
# =========================================================

from memory_v8 import (
    get_memory,
)

from memory_intent import (
    resolve_memory_key,
)

from memory_semantic_rag import (
    search_semantic_memory,
)

from memory_semantic_resolver import (
    resolve_memory_result,
)


# =========================================================
# HYBRID MEMORY SEARCH
# =========================================================

def retrieve_memory(
    question,
    memory_vector_store,
    memory_data,
):
    """
    Retrieval priority:

        1. Exact structured memory
        2. Semantic memory
        3. No memory
    """

    if not question or not question.strip():
        return None

    # =====================================================
    # 1. EXACT STRUCTURED MEMORY
    # =====================================================

    key = resolve_memory_key(
        question
    )

    if key:

        exact = get_memory(
            memory_data,
            key
        )

        if exact:

            result = dict(
                exact
            )

            result["retrieval_method"] = (
                "structured"
            )

            return result

    # =====================================================
    # 2. SEMANTIC MEMORY
    # =====================================================

    semantic_results = search_semantic_memory(
        question,
        memory_vector_store,
        top_k=1,
    )

    if semantic_results:

        resolved = resolve_memory_result(
            semantic_results[0]
        )

        if resolved:

            resolved["retrieval_method"] = (
                "semantic"
            )

            return resolved

    # =====================================================
    # 3. NO MEMORY
    # =====================================================

    return None