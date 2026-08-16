# =========================================================
# JARVIS V8.6.3 - ROUTE DETECTOR
# =========================================================

from memory_intent import resolve_memory_key


def detect_route(command):
    """
    Estimate which JARVIS subsystem is expected to handle
    a command.

    This is an observability classifier only.
    It does NOT execute the command and does NOT change
    brain.py routing.
    """

    if not command:
        return "model"

    text = command.lower().strip()

    # -----------------------------------------------------
    # MEMORY
    # -----------------------------------------------------

    memory_key = resolve_memory_key(
        text
    )

    if memory_key:
        return "memory"

    # -----------------------------------------------------
    # RAG / KNOWLEDGE
    # -----------------------------------------------------

    rag_patterns = [
        "how does v5",
        "what does v3",
        "what is v4",
        "according to",
        "according to jarvis",
    ]

    for pattern in rag_patterns:

        if pattern in text:
            return "rag"

    # -----------------------------------------------------
    # MCP
    # -----------------------------------------------------

    mcp_patterns = [
        "mcp",
        "jarvis mcp",
        "mcp server",
    ]

    for pattern in mcp_patterns:

        if pattern in text:
            return "mcp"

    # -----------------------------------------------------
    # NATIVE TOOL
    # -----------------------------------------------------

    native_patterns = [
        "open youtube",
        "open google",
        "open notepad",
        "open calculator",
        "open powershell",
        "open downloads",
        "search youtube",
        "search google",
    ]

    for pattern in native_patterns:

        if pattern in text:
            return "native"

    # -----------------------------------------------------
    # NORMAL MODEL
    # -----------------------------------------------------

    return "model"