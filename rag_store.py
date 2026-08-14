# =========================================================
# JARVIS V4.4 - RAG STORE
# =========================================================

from document_chunker import chunk_text
from embeddings import embed_texts
from vector_store import VectorStore

vector_store=VectorStore()

# =========================================================
# ADD DOCUMENT TO KNOWLEDGE BASE
# =========================================================

def add_document(
    text,
    source="unknown",
    chunk_size=500,
    overlap=100
):

    chunks = chunk_text(
        text,
        chunk_size=chunk_size,
        overlap=overlap
    )

    if not chunks:
        return 0

    embeddings = embed_texts(
        chunks
    )

    added_count = 0

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        added = vector_store.add(
            text=chunk,
            embedding=embedding,
            metadata={
                "source": source
            }
        )

        if added:
            added_count += 1

    if added_count:
        vector_store.save()

    return added_count

# =========================================================
# SEARCH KNOWLEDGE BASE
# =========================================================

def search_knowledge(
    query,
    top_k=3,
    min_score=0.70
):

    query_embedding = embed_texts(
        [query]
    )[0]

    results = vector_store.search(
        query_embedding=query_embedding,
        top_k=top_k
    )

    if min_score is None:
        return results

    return [
        result
        for result in results
        if result["score"] >= min_score
    ]

