# =========================================================
# JARVIS V8.2.2 - PERSISTENT MEMORY VECTOR STORE
# =========================================================

import json
import os


MEMORY_VECTOR_FILE = "memory_vectors.json"


# =========================================================
# CREATE EMPTY STORE
# =========================================================

def create_memory_vector_store():

    return {
        "memories": []
    }


# =========================================================
# LOAD STORE
# =========================================================

def load_memory_vector_store():

    if not os.path.exists(
        MEMORY_VECTOR_FILE
    ):
        return create_memory_vector_store()

    try:

        with open(
            MEMORY_VECTOR_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

    except (
        OSError,
        json.JSONDecodeError
    ):

        return create_memory_vector_store()

    if (
        isinstance(data, dict)
        and isinstance(
            data.get("memories"),
            list
        )
    ):
        return data

    return create_memory_vector_store()


# =========================================================
# SAVE STORE
# =========================================================

def save_memory_vector_store(store):

    with open(
        MEMORY_VECTOR_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            store,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# ADD OR UPDATE MEMORY VECTOR
# =========================================================

def add_or_update_memory_vector(
    store,
    memory_id,
    text,
    embedding
):

    for item in store["memories"]:

        if item.get(
            "memory_id"
        ) == memory_id:

            item["text"] = text

            item["embedding"] = embedding

            return item

    item = {
        "memory_id": memory_id,
        "text": text,
        "embedding": embedding,
    }

    store["memories"].append(
        item
    )

    return item


# =========================================================
# GET MEMORY VECTOR
# =========================================================

def get_memory_vector(
    store,
    memory_id
):

    for item in store.get(
        "memories",
        []
    ):

        if item.get(
            "memory_id"
        ) == memory_id:

            return item

    return None


# =========================================================
# GET ALL MEMORY VECTORS
# =========================================================

def get_all_memory_vectors(
    store
):

    return store.get(
        "memories",
        []
    )