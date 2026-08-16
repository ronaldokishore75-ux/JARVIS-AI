# =========================================================
# JARVIS V9.1.7 - CONVERSATION CONTEXT MANAGER
# =========================================================

from conversation_context import (
    add_turn,
    get_recent_turns,
    load_context,
    save_context,
)


class ConversationContextManager:

    def __init__(
        self,
        filepath="context.json",
    ):
        self.filepath = filepath
        self.context = load_context(
            filepath
        )

    # =====================================================
    # CONVERSATION
    # =====================================================

    def add_turn(
        self,
        user_message,
        assistant_response,
    ):
        add_turn(
            self.context,
            user_message,
            assistant_response,
        )

    def get_recent_turns(
        self,
        limit=5,
    ):
        return get_recent_turns(
            self.context,
            limit,
        )

    # =====================================================
    # ACTIVE APP
    # =====================================================

    def set_active_app(
        self,
        app,
    ):
        self.context["active_app"] = app

    def get_active_app(self):
        return self.context.get(
            "active_app"
        )

    # =====================================================
    # ACTIVE TOOL
    # =====================================================

    def set_active_tool(
        self,
        tool,
    ):
        self.context["active_tool"] = tool

    def get_active_tool(self):
        return self.context.get(
            "active_tool"
        )

    # =====================================================
    # ACTIVE TASK
    # =====================================================

    def set_active_task(
        self,
        task,
    ):
        self.context["active_task"] = task

    def get_active_task(self):
        return self.context.get(
            "active_task"
        )

    # =====================================================
    # LAST ACTION
    # =====================================================

    def set_last_action(
        self,
        action,
    ):
        self.context["last_action"] = action

    def get_last_action(self):
        return self.context.get(
            "last_action"
        )

    # =====================================================
    # CLEAR ACTIVE STATE
    # =====================================================

    def clear_active_state(self):
        self.context["active_task"] = None
        self.context["active_app"] = None
        self.context["active_tool"] = None
        self.context["last_action"] = None

    # =====================================================
    # SAVE
    # =====================================================

    def save(self):
        save_context(
            self.context,
            self.filepath,
        )

    # =====================================================
    # RELOAD
    # =====================================================

    def reload(self):
        self.context = load_context(
            self.filepath
        )