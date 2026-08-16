# =========================================================
# JARVIS V8.1.5 - PERSISTENT MEMORY + RETRIEVAL
# =========================================================

import json
import os
from datetime import datetime


MEMORY_FILE = "memory.json"

ALLOWED_SOURCES = {
    "user",
    "system",
    "imported",
    "migration",
}


# =========================================================
# CREATE EMPTY MEMORY
# =========================================================

def create_memory():

    return {
        "memories": []
    }


# =========================================================
# CURRENT TIMESTAMP
# =========================================================

def current_timestamp():

    return datetime.now().isoformat(
        timespec="seconds"
    )


# =========================================================
# VALIDATE SOURCE
# =========================================================

def validate_source(source):

    if source not in ALLOWED_SOURCES:

        raise ValueError(
            f"Invalid memory source: {source}. "
            f"Allowed sources: "
            f"{sorted(ALLOWED_SOURCES)}"
        )

    return source


# =========================================================
# LOAD MEMORY
# =========================================================

def load_memory():

    if not os.path.exists(
        MEMORY_FILE
    ):

        return create_memory()

    try:

        with open(
            MEMORY_FILE,
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

        return create_memory()


    # -----------------------------------------------------
    # V8 FORMAT
    # -----------------------------------------------------

    if (
        isinstance(data, dict)
        and "memories" in data
        and isinstance(
            data["memories"],
            list
        )
    ):

        return {
            "memories": data["memories"]
        }

    # -----------------------------------------------------
    # LEGACY FORMAT MIGRATION
    # -----------------------------------------------------

    if isinstance(data, dict):

        migrated = create_memory()

        for key, value in data.items():

            timestamp = current_timestamp()

            migrated["memories"].append(
                {
                    "id": (
                        f"memory_"
                        f"{len(migrated['memories']) + 1:03d}"
                    ),
                    "category": "legacy",
                    "key": key,
                    "value": value,
                    "source": "migration",
                    "created_at": timestamp,
                    "updated_at": timestamp,
                }
            )

        return migrated


    return create_memory()


# =========================================================
# SAVE MEMORY
# =========================================================

def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# FIND MEMORY BY KEY
# =========================================================

def find_memory(
    memory,
    key
):

    for item in memory.get(
        "memories",
        []
    ):

        if item.get(
            "key"
        ) == key:

            return item

    return None


# =========================================================
# GET MEMORY BY KEY
# =========================================================

def get_memory(
    memory,
    key
):

    return find_memory(
        memory,
        key
    )


# =========================================================
# GET MEMORIES BY CATEGORY
# =========================================================

def get_memories_by_category(
    memory,
    category
):

    return [
        item
        for item in memory.get(
            "memories",
            []
        )
        if item.get(
            "category"
        ) == category
    ]


# =========================================================
# GET MEMORIES BY SOURCE
# =========================================================

def get_memories_by_source(
    memory,
    source
):

    validate_source(
        source
    )

    return [
        item
        for item in memory.get(
            "memories",
            []
        )
        if item.get(
            "source"
        ) == source
    ]


# =========================================================
# ADD OR UPDATE MEMORY
# =========================================================

def add_or_update_memory(
    memory,
    key,
    value,
    category="general",
    source="user"
):

    validate_source(
        source
    )

    existing = find_memory(
        memory,
        key
    )

    timestamp = current_timestamp()


    # -----------------------------------------------------
    # UPDATE EXISTING MEMORY
    # -----------------------------------------------------

    if existing:

        existing["value"] = value

        existing["category"] = category

        existing["source"] = source

        existing["updated_at"] = timestamp

        return existing


    # -----------------------------------------------------
    # CREATE NEW MEMORY
    # -----------------------------------------------------

    new_memory = {
        "id": (
            f"memory_"
            f"{len(memory['memories']) + 1:03d}"
        ),
        "category": category,
        "key": key,
        "value": value,
        "source": source,
        "created_at": timestamp,
        "updated_at": timestamp,
    }

    memory["memories"].append(
        new_memory
    )

    return new_memory