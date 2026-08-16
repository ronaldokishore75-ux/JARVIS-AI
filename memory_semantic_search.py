# =========================================================
# JARVIS V8.2.5 - SEMANTIC MEMORY SEARCH + CONFIDENCE
# =========================================================

import math


# =========================================================
# COSINE SIMILARITY
# =========================================================

def cosine_similarity(
    vector_a,
    vector_b
):
    """
    Calculate cosine similarity between two vectors.
    """

    if not vector_a or not vector_b:
        return 0.0

    if len(vector_a) != len(vector_b):
        raise ValueError(
            "Vectors must have the same length."
        )

    dot_product = sum(
        a * b
        for a, b in zip(
            vector_a,
            vector_b
        )
    )

    magnitude_a = math.sqrt(
        sum(
            value * value
            for value in vector_a
        )
    )

    magnitude_b = math.sqrt(
        sum(
            value * value
            for value in vector_b
        )
    )

    if (
        magnitude_a == 0
        or magnitude_b == 0
    ):
        return 0.0

    return (
        dot_product
        / (
            magnitude_a
            * magnitude_b
        )
    )


# =========================================================
# SEARCH MEMORY VECTORS
# =========================================================

def search_memory_vectors(
    query_embedding,
    memory_vectors,
    top_k=3,
    min_score=0.60
):
    """
    Rank memory vectors by cosine similarity and only
    return results meeting the confidence threshold.
    """

    results = []

    for item in memory_vectors:

        embedding = item.get(
            "embedding",
            []
        )

        score = cosine_similarity(
            query_embedding,
            embedding
        )

        if score < min_score:
            continue

        results.append(
            {
                "memory_id": item["memory_id"],
                "text": item["text"],
                "score": score,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]