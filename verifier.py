# =========================================================
# JARVIS V5.6 - GOAL VERIFIER
# =========================================================

def verify_step(action, value, result):
    """
    Decide whether a completed action should be considered
    successful.

    This first version uses simple, deterministic checks.
    """

    # -----------------------------------------------------
    # Generic failure
    # -----------------------------------------------------

    if result is None:
        return False

    if result is False:
        return False

    if isinstance(result, str):

        lowered = result.lower()

        failure_words = [
            "couldn't",
            "failed",
            "error",
            "not found",
            "unable",
        ]

        if any(
            word in lowered
            for word in failure_words
        ):
            return False

    # -----------------------------------------------------
    # Known actions
    # -----------------------------------------------------

    if action == "open_youtube":

        return (
            isinstance(result, str)
            and "opening youtube" in result.lower()
        )

    if action == "search_youtube":

        return (
            isinstance(result, str)
            and "searching youtube" in result.lower()
        )

    if action == "scroll_down":

        return (
            isinstance(result, str)
            and "scrolling down" in result.lower()
        )

    if action == "click_link":

        return (
            isinstance(result, str)
            and "clicking" in result.lower()
        )

    # -----------------------------------------------------
    # Default
    # -----------------------------------------------------

    return True