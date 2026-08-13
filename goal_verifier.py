# =========================================================
# JARVIS V5.7 - GOAL VERIFIER
# =========================================================

def verify_goal(goal, results):
    """
    Verify whether the overall task appears to have
    completed successfully.

    First version is deterministic and based on the
    results returned by the task runner.
    """

    if not goal:
        return False

    if not results:
        return False

    # Any explicit failure means the overall goal failed.
    for result in results:

        if result is None or result is False:
            return False

        if isinstance(result, str):

            lowered = result.lower()

            failure_words = [
                "couldn't",
                "failed",
                "error",
                "not found",
                "unable",
                "cancelled",
            ]

            if any(
                word in lowered
                for word in failure_words
            ):
                return False

    # If every step produced a valid result,
    # consider the goal completed for now.
    return True