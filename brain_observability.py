# =========================================================
# JARVIS V8.6.5 - ROUTE MATCH OBSERVABILITY
# =========================================================

import io
import time
from contextlib import redirect_stdout

from observability import create_event, log_event
from route_detector import detect_route


def detect_actual_route(debug_output, response):
    text = debug_output or ""
    answer = str(response or "")

    if (
        "Your name is" in answer
        or "Your favorite color is" in answer
        or "You live in" in answer
    ):
        return "memory"

    if "V4 RAG: Relevant knowledge found." in text:
        return "rag"

    if "V7.5 MCP TOOL CALL:" in text:
        return "mcp"

    if (
        "DEBUG: intent= open_youtube" in text
        or "DEBUG: intent= open_google" in text
        or "DEBUG: intent= search_youtube" in text
        or "DEBUG: intent= search_google" in text
        or "Opening YouTube" in text
        or "Opening Google" in text
    ):
        return "native"

    if "V7.8 ROUTER: No tool required." in text:
        return "model"

    return "unknown"


def observe_brain_request(brain_function, command):

    start_time = time.perf_counter()

    response = None
    error = None
    success = False

    predicted_route = detect_route(command)

    print(
        f"V8.6.5 PREDICTED ROUTE: {predicted_route}"
    )

    buffer = io.StringIO()

    try:
        with redirect_stdout(buffer):
            response = brain_function(command)

        success = response is not None

    except Exception as exc:
        error = repr(exc)
        raise

    finally:
        debug_output = buffer.getvalue()

        print(
            debug_output,
            end=""
        )

        actual_route = detect_actual_route(
            debug_output,
            response
        )

        route_match = (
            predicted_route == actual_route
        )

        latency_ms = round(
            (
                time.perf_counter()
                - start_time
            ) * 1000,
            2,
        )

        print(
            f"V8.6.5 ACTUAL ROUTE: {actual_route}"
        )

        print(
            f"V8.6.5 ROUTE MATCH: {route_match}"
        )

        event = create_event(
            command=command,
            route=actual_route,
            success=success,
            latency_ms=latency_ms,
            error=error,
            metadata={
                "predicted_route": predicted_route,
                "actual_route": actual_route,
                "route_match": route_match,
                "response_type": (
                    type(response).__name__
                    if response is not None
                    else None
                ),
            },
        )

        log_event(event)

    return response
