# =========================================================
# JARVIS V8.1.8 - MEMORY INTENT RESOLUTION
# =========================================================

import re


MEMORY_RULES = [

    # -----------------------------------------------------
    # FAVORITE COLOR
    # -----------------------------------------------------

    {
        "key": "favorite_color",
        "patterns": [
            r"\bfavorite color\b",
            r"\bfavorite colour\b",
            r"\bcolor i like\b",
            r"\bcolour i like\b",
            r"\bwhat color do i like\b",
            r"\bwhat colour do i like\b",
        ],
    },

    # -----------------------------------------------------
    # NAME
    # -----------------------------------------------------

    {
        "key": "name",
        "patterns": [
            r"\bmy name\b",
            r"\bwhat is my name\b",
            r"\bwhat's my name\b",
            r"\bdo you remember my name\b",
        ],
    },

    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    {
        "key": "location",
        "patterns": [
            r"\bmy location\b",
            r"\bwhere do i live\b",
            r"\bwhere am i from\b",
            r"\bwhich city do i live in\b",
            r"\bwhat city do i live in\b",
            r"\bdo you remember where i live\b",
            r"\bwhat is my location\b",
            r"\bwhat's my location\b",
        ],
    },
]


# =========================================================
# RESOLVE MEMORY KEY
# =========================================================

def resolve_memory_key(question):

    if not question:
        return None

    text = question.lower().strip()

    for rule in MEMORY_RULES:

        for pattern in rule["patterns"]:

            if re.search(
                pattern,
                text
            ):
                return rule["key"]

    return None