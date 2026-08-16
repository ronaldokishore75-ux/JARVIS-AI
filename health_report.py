# =========================================================
# JARVIS V8.6.7 - HEALTH REPORT
# =========================================================

from observability_metrics import (
    load_events,
    calculate_metrics,
)


def generate_health_report(
    filepath="observability.jsonl"
):
    events = load_events(
        filepath
    )

    metrics = calculate_metrics(
        events
    )

    lines = []

    lines.append(
        "=" * 60
    )

    lines.append(
        "JARVIS HEALTH REPORT"
    )

    lines.append(
        "=" * 60
    )

    # -----------------------------------------------------
    # Overall metrics
    # -----------------------------------------------------

    lines.append(
        f"Requests:           "
        f"{metrics['total_requests']}"
    )

    lines.append(
        f"Successful:         "
        f"{metrics['successful_requests']}"
    )

    lines.append(
        f"Failed:             "
        f"{metrics['failed_requests']}"
    )

    lines.append(
        f"Success rate:       "
        f"{metrics['success_rate']:.2f}%"
    )

    lines.append(
        f"Route mismatches:   "
        f"{metrics['route_mismatches']}"
    )

    lines.append(
        f"Average latency:    "
        f"{metrics['average_latency_ms']:.2f} ms"
    )

    # -----------------------------------------------------
    # Route metrics
    # -----------------------------------------------------

    route_data = metrics.get(
        "by_route",
        {}
    )

    if route_data:

        lines.append(
            "\nROUTES:"
        )

        fastest_route = None
        fastest_latency = None

        slowest_route = None
        slowest_latency = None

        for route, data in route_data.items():

            lines.append(
                f"  {route:<12} "
                f"{data['success_rate']:>6.2f}% success | "
                f"{data['average_latency_ms']:>10.2f} ms | "
                f"{data['requests']} requests"
            )

            latency = data[
                "average_latency_ms"
            ]

            if fastest_latency is None or (
                latency < fastest_latency
            ):
                fastest_latency = latency
                fastest_route = route

            if slowest_latency is None or (
                latency > slowest_latency
            ):
                slowest_latency = latency
                slowest_route = route

        # -------------------------------------------------
        # Fastest / slowest
        # -------------------------------------------------

        if fastest_route:

            lines.append(
                "\nFASTEST ROUTE:"
            )

            lines.append(
                f"  {fastest_route} "
                f"({fastest_latency:.2f} ms)"
            )

        if slowest_route:

            lines.append(
                "\nSLOWEST ROUTE:"
            )

            lines.append(
                f"  {slowest_route} "
                f"({slowest_latency:.2f} ms)"
            )

    # -----------------------------------------------------
    # Health status
    # -----------------------------------------------------

    healthy = True

    if metrics["failed_requests"] > 0:
        healthy = False

    if metrics["route_mismatches"] > 0:
        healthy = False

    if healthy:

        status = "JARVIS HEALTHY"

    else:

        status = "JARVIS NEEDS ATTENTION"

    lines.append(
        "\nSTATUS:"
    )

    lines.append(
        f"  {status}"
    )

    lines.append(
        "=" * 60
    )

    return "\n".join(
        lines
    )