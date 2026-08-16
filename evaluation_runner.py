# =========================================================
# JARVIS V8.7.2 - EVALUATION RUNNER
# =========================================================

import io

from contextlib import redirect_stdout

from brain import jarvis_response

from route_detector import (
    detect_route,
)

from brain_observability import (
    detect_actual_route,
)

from evaluation import (
    EvaluationCase,
    EvaluationResult,
)


def run_evaluation_case(
    case: EvaluationCase,
):
    """
    Run one real brain request and evaluate:
        - predicted route
        - actual route
        - response
        - required debug markers
        - forbidden debug markers
    """

    errors = []

    buffer = io.StringIO()

    with redirect_stdout(buffer):

        response = jarvis_response(
            case.command
        )

    debug_output = buffer.getvalue()

    predicted_route = detect_route(
        case.command
    )

    actual_route = detect_actual_route(
        debug_output,
        response,
    )

    # -----------------------------------------------------
    # ROUTE
    # -----------------------------------------------------

    route_ok = True

    if case.expected_route is not None:

        route_ok = (
            actual_route
            == case.expected_route
        )

        if not route_ok:

            errors.append(
                "Expected route "
                f"{case.expected_route}, "
                f"got {actual_route}."
            )

    # -----------------------------------------------------
    # RESPONSE
    # -----------------------------------------------------

    response_text = str(
        response
        or ""
    )

    response_ok = True

    if case.expected_response is not None:

        response_ok = (
            case.expected_response
            in response_text
        )

        if not response_ok:

            errors.append(
                "Expected response text was "
                "not found."
            )

    # -----------------------------------------------------
    # REQUIRED DEBUG
    # -----------------------------------------------------

    required_debug_ok = True

    for marker in case.required_debug:

        if marker not in debug_output:

            required_debug_ok = False

            errors.append(
                f"Missing required debug marker: "
                f"{marker}"
            )

    # -----------------------------------------------------
    # FORBIDDEN DEBUG
    # -----------------------------------------------------

    forbidden_debug_ok = True

    for marker in case.forbidden_debug:

        if marker in debug_output:

            forbidden_debug_ok = False

            errors.append(
                f"Forbidden debug marker found: "
                f"{marker}"
            )

    passed = (
        route_ok
        and response_ok
        and required_debug_ok
        and forbidden_debug_ok
    )

    return EvaluationResult(
        name=case.name,
        passed=passed,
        route_ok=route_ok,
        response_ok=response_ok,
        required_debug_ok=required_debug_ok,
        forbidden_debug_ok=forbidden_debug_ok,
        response=response_text,
        debug_output=debug_output,
        errors=errors,
    )