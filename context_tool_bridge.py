# =========================================================
# JARVIS V9.1.6 - CONTEXT TOOL BRIDGE
# =========================================================

from action import (
    scroll_down,
    scroll_up,
    scroll_down_little,
    scroll_up_little,
)


CONTEXT_ACTIONS = {
    "scroll_down": scroll_down,
    "scroll_up": scroll_up,
    "scroll_down_little": scroll_down_little,
    "scroll_up_little": scroll_up_little,
}


def execute_context_action(
    resolved_command,
):
    """
    Execute a normalized V9 contextual action through
    the existing native action layer.
    """

    if not resolved_command:
        return {
            "success": False,
            "message": "No contextual action.",
        }

    action_name = resolved_command.get(
        "action"
    )

    action = CONTEXT_ACTIONS.get(
        action_name
    )

    if not action:
        return {
            "success": False,
            "message": (
                f"Unsupported context action: "
                f"{action_name}"
            ),
        }

    try:

        action()

        return {
            "success": True,
            "action": action_name,
            "source": "context",
            "message": (
                f"Context action '{action_name}' "
                f"executed successfully."
            ),
        }

    except Exception as error:

        return {
            "success": False,
            "action": action_name,
            "source": "context",
            "error": repr(error),
        }