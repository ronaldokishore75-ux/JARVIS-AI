# =========================================================
# JARVIS V9.1.7 - CONVERSATION CONTEXT
# =========================================================

import json
import os
from datetime import datetime


CONTEXT_FILE = "context.json"


def create_context():
    return {
        "turns": [],
        "active_task": None,
        "active_app": None,
        "active_tool": None,
        "last_action": None,
    }


def current_timestamp():
    return datetime.now().isoformat(
        timespec="seconds"
    )


def add_turn(
    context,
    user_message,
    assistant_response,
):
    context["turns"].append(
        {
            "timestamp": current_timestamp(),
            "user": user_message,
            "assistant": assistant_response,
        }
    )


def get_recent_turns(
    context,
    limit=5,
):
    return context.get(
        "turns",
        []
    )[-limit:]


def save_context(
    context,
    filepath=CONTEXT_FILE,
):
    with open(
        filepath,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            context,
            file,
            indent=4,
            ensure_ascii=False,
        )


def load_context(
    filepath=CONTEXT_FILE,
):
    if not os.path.exists(filepath):
        return create_context()

    try:
        with open(
            filepath,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

    except (
        OSError,
        json.JSONDecodeError,
    ):
        return create_context()

    if not isinstance(data, dict):
        return create_context()

    if not isinstance(
        data.get("turns"),
        list,
    ):
        data["turns"] = []

    if "active_task" not in data:
        data["active_task"] = None

    if "active_app" not in data:
        data["active_app"] = None

    if "active_tool" not in data:
        data["active_tool"] = None

    if "last_action" not in data:
        data["last_action"] = None

    return data