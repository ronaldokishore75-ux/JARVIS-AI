# =========================================================
# JARVIS V8.2.6 - SEMANTIC MEMORY RESOLVER
# =========================================================

from memory_v8 import load_memory


def resolve_memory_result(
    search_result
):
    """
    Convert a semantic-search result into the complete
    stored V8 memory record while preserving the score.
    """

    if not search_result:

        return None

    memory_id = search_result.get(
        "memory_id"
    )

    score = search_result.get(
        "score"
    )

    if not memory_id:

        return None

    memory = load_memory()

    for item in memory.get(
        "memories",
        []
    ):

        if item.get(
            "id"
        ) == memory_id:

            resolved = dict(
                item
            )

            resolved["score"] = score

            return resolved

    return None