# =========================================================
# JARVIS V8.4 - MEMORY WRITE INTEGRATION
# =========================================================

from memory_v8 import (
    load_memory,
    save_memory,
    add_or_update_memory,
)


# =========================================================
# SAVE USER MEMORY
# =========================================================

def remember_user_memory(
    key,
    value,
    category="general",
):
    """
    Save or update a user memory using the V8 memory system.
    """

    memory = load_memory()

    result = add_or_update_memory(
        memory,
        key,
        value,
        category=category,
        source="user",
    )

    save_memory(
        memory
    )

    return result


# =========================================================
# REMEMBER NAME
# =========================================================

def remember_name(
    name
):
    return remember_user_memory(
        "name",
        name,
        category="identity",
    )


# =========================================================
# REMEMBER FAVORITE COLOR
# =========================================================

def remember_favorite_color(
    color
):
    return remember_user_memory(
        "favorite_color",
        color,
        category="preference",
    )


# =========================================================
# REMEMBER LOCATION
# =========================================================

def remember_location(
    city
):
    return remember_user_memory(
        "location",
        city,
        category="location",
    )