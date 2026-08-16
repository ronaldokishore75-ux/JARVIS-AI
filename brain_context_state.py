# =========================================================
# JARVIS V9.1.16 - BRAIN CONTEXT STATE
# =========================================================

from context_state_updater import (
    update_context_from_action,
)


def update_from_brain_action(
    context_integration,
    action,
    success=True,
):
    """
    Update V9 context state after a brain/native action.
    """

    if not action:
        return context_integration.get_context()

    update_context_from_action(
        context_integration.manager,
        action,
        success=success,
    )

    context_integration.manager.save()

    return context_integration.get_context()


def record_brain_turn(
    context_integration,
    user_message,
    assistant_response,
):
    """
    Record one completed brain interaction.
    """

    if user_message is None:
        return context_integration.get_context()

    if assistant_response is None:
        return context_integration.get_context()

    context_integration.manager.add_turn(
        user_message,
        str(assistant_response),
    )

    context_integration.manager.save()

    return context_integration.get_context()