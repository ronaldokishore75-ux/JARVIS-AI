# =========================================================
# JARVIS V9.1.5 / V9.1.11 - CONTEXT COMMAND RESOLVER
# =========================================================

from context_reference_resolver import (
    resolve_reference,
)


def resolve_context_command(
    command,
    context,
):
    """
    Convert a context-dependent command into a
    normalized JARVIS action.
    """

    result = resolve_reference(
        command,
        context,
    )

    if not result:
        return None

    action = result.get(
        "action"
    )

    action_map = {
        "scroll_down": "scroll_down",
        "scroll_up": "scroll_up",
        "scroll_down_little": "scroll_down_little",
        "scroll_up_little": "scroll_up_little",
    }

    normalized_action = action_map.get(
        action
    )

    if not normalized_action:
        return None

    return {
        "action": normalized_action,
        "app": result.get(
            "app"
        ),
        "source": "context",
        "active_tool": result.get(
            "active_tool"
        ),
    }