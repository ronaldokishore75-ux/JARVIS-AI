# =========================================================
# JARVIS V9.1.17 - BRAIN WITH CONVERSATION CONTEXT
# =========================================================

from brain import jarvis_response as _jarvis_response

from brain import (
    context_integration,
)

from brain_turn_observability import (
    record_completed_turn,
)


def jarvis_response_with_context(
    command,
    _task_step=False,
):
    """
    Run the existing brain and record the conversation turn.

    The original user command is preserved in context history.
    Contextual commands are recorded by the V9 bridge itself,
    so they are not recorded twice.
    """

    original_command = command

    before_count = len(
        context_integration.get_context()["turns"]
    )

    response = _jarvis_response(
        command,
        _task_step=_task_step,
    )

    after_count = len(
        context_integration.get_context()["turns"]
    )

    context_already_recorded = (
        after_count > before_count
    )

    if context_already_recorded:

        # V9 contextual handling used the normalized command.
        # Replace that stored user text with the original wording.
        turns = context_integration.get_context()["turns"]

        if turns:

            turns[-1]["user"] = original_command

            context_integration.manager.save()

    else:

        record_completed_turn(
            context_integration,
            original_command,
            response,
        )

    return response