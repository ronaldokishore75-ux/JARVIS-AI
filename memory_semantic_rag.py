# =========================================================
# JARVIS V8.2.4 - REAL SEMANTIC MEMORY SEARCH
# =========================================================

from embeddings import embed_text

from memory_embeddings import (
    memory_to_text,
)

from memory_vector_store import (
    create_memory_vector_store,
    add_or_update_memory_vector,
    save_memory_vector_store,
    load_memory_vector_store,
)

from memory_semantic_search import (
    search_memory_vectors,
)


# =========================================================
# BUILD MEMORY VECTOR STORE
# =========================================================

def build_memory_vector_store(
    memories
):
    """
    Convert V8 memories into real embeddings and store them.
    """

    store = create_memory_vector_store()

    for memory in memories:

        text = memory_to_text(
            memory
        )

        embedding = embed_text(
            text
        )

        add_or_update_memory_vector(
            store,
            memory["id"],
            text,
            embedding,
        )

    return store


# =========================================================
# SEMANTIC MEMORY SEARCH
# =========================================================

def search_semantic_memory(
    query,
    memory_vector_store,
    top_k=3,
):
    """
    Embed the query and search real memory vectors.
    """

    query_embedding = embed_text(
        query
    )

    vectors = memory_vector_store.get(
        "memories",
        []
    )

    return search_memory_vectors(
        query_embedding,
        vectors,
        top_k=top_k,
    )


# =========================================================
# SAVE MEMORY VECTOR STORE
# =========================================================

def save_semantic_memory_store(
    memories
):
    """
    Build and persist the real memory vector store.
    """

    store = build_memory_vector_store(
        memories
    )

    save_memory_vector_store(
        store
    )

    return store