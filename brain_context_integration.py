# =========================================================
# JARVIS V9.1.9 - BRAIN CONTEXT INTEGRATION
# =========================================================

from conversation_context_manager import (
    ConversationContextManager,
)

from context_command_resolver import (
    resolve_context_command,
)

from context_tool_bridge import (
    execute_context_action,
)

from context_state_updater import (
    update_context_from_action,
)


class BrainContextIntegration:

    def __init__(
        self,
        filepath="context.json",
    ):
        self.manager = ConversationContextManager(
            filepath
        )

    # =====================================================
    # CONTEXTUAL COMMAND
    # =====================================================

    def try_context_command(
        self,
        command,
    ):
        """
        Try to resolve and execute a command using
        the active conversation context.

        Returns:
            response dict or None
        """

        resolved = resolve_context_command(
            command,
            self.manager.context,
        )

        if not resolved:
            return None

        result = execute_context_action(
            resolved
        )

        if result.get("success"):

            update_context_from_action(
                self.manager,
                resolved["action"],
                success=True,
            )

            response = {
                "success": True,
                "source": "context",
                "action": resolved["action"],
                "message": result.get(
                    "message",
                    "Context action executed.",
                ),
            }

        else:

            response = {
                "success": False,
                "source": "context",
                "action": resolved.get(
                    "action"
                ),
                "message": result.get(
                    "message",
                    "Context action failed.",
                ),
            }

        self.manager.add_turn(
            command,
            response["message"],
        )

        self.manager.save()

        return response

    # =====================================================
    # RECORD NORMAL BRAIN TURN
    # =====================================================

    def record_brain_turn(
        self,
        command,
        response,
        action=None,
        success=True,
    ):
        """
        Record a normal brain interaction and optionally
        update active state.
        """

        if action and success:

            update_context_from_action(
                self.manager,
                action,
                success=True,
            )

        self.manager.add_turn(
            command,
            response,
        )

        self.manager.save()

        return self.manager.context

    # =====================================================
    # CONTEXT ACCESS
    # =====================================================

    def get_context(self):
        return self.manager.context