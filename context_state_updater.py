# =========================================================
# JARVIS V9.1.7 - CONTEXT STATE UPDATER
# =========================================================


def update_context_from_action(
    manager,
    action,
    success=True,
):
    """
    Update conversation context after an action.

    Only successful actions change active state.
    """

    if not success:
        return manager.context

    action = action or ""

    # -----------------------------------------------------
    # YouTube
    # -----------------------------------------------------

    if action == "open_youtube":
        manager.set_active_app(
            "youtube"
        )

    elif action == "search_youtube":
        manager.set_active_app(
            "youtube"
        )
        manager.set_active_tool(
            "search_youtube"
        )

    # -----------------------------------------------------
    # Google
    # -----------------------------------------------------

    elif action == "open_google":
        manager.set_active_app(
            "google"
        )

    elif action == "search_google":
        manager.set_active_app(
            "google"
        )
        manager.set_active_tool(
            "search_google"
        )

    # -----------------------------------------------------
    # Generic contextual actions
    # -----------------------------------------------------

    if action:
        manager.set_last_action(
            action
        )

    return manager.context