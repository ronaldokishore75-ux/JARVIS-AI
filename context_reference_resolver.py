# =========================================================
# JARVIS V9.1.11 - CONTEXT REFERENCE RESOLVER
# =========================================================

def resolve_reference(
    command,
    context,
):

    if not command:
        return None

    text = command.lower().strip()

    text = text.rstrip(
        ".!?"
    ).strip()

    active_app = context.get(
        "active_app"
    )

    active_tool = context.get(
        "active_tool"
    )

    # =====================================================
    # YOUTUBE CONTEXT
    # =====================================================

    if active_app == "youtube":

        if text in {
            "scroll down",
            "scroll down a little",
            "go lower",
            "move lower",
        }:

            return {
                "resolved": True,
                "app": "youtube",
                "action": "scroll_down",
                "active_tool": active_tool,
            }

        if text in {
            "scroll up",
            "scroll up a little",
            "go higher",
            "move higher",
        }:

            return {
                "resolved": True,
                "app": "youtube",
                "action": "scroll_up",
                "active_tool": active_tool,
            }

    return None