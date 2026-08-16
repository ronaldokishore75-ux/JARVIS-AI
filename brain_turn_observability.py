# =========================================================
# JARVIS V9.1.17 - BRAIN TURN OBSERVABILITY
# =========================================================

from brain_context_state import (
    record_brain_turn,
)


def record_completed_turn(
    context_integration,
    command,
    response,
):
    """
    Record a completed brain interaction.

    This only records a turn when both the command and
    response are available.
    """

    if command is None:
        return context_integration.get_context()

    if response is None:
        return context_integration.get_context()

    record_brain_turn(
        context_integration,
        command,
        response,
    )

    return context_integration.get_context()