# =========================================================
# JARVIS V8.6.6 - OBSERVABILITY METRICS
# =========================================================

import json
import os
from collections import defaultdict


DEFAULT_FILE = "observability.jsonl"


def load_events(filepath=DEFAULT_FILE):

    if not os.path.exists(filepath):
        return []

    events = []

    with open(
        filepath,
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            try:
                events.append(
                    json.loads(line)
                )

            except json.JSONDecodeError:
                continue

    return events


def calculate_metrics(events):

    total = len(events)

    successful = sum(
        1
        for event in events
        if event.get("success") is True
    )

    failed = total - successful

    latencies = [
        event["latency_ms"]
        for event in events
        if isinstance(
            event.get("latency_ms"),
            (int, float)
        )
    ]

    average_latency = (
        round(
            sum(latencies) / len(latencies),
            2,
        )
        if latencies
        else 0.0
    )

    mismatches = sum(
        1
        for event in events
        if event.get("metadata", {}).get(
            "route_match"
        ) is False
    )

    by_route = defaultdict(
        lambda: {
            "requests": 0,
            "successes": 0,
            "failures": 0,
            "latencies": [],
            "route_mismatches": 0,
        }
    )

    for event in events:

        route = event.get(
            "route",
            "unknown"
        )

        data = by_route[route]

        data["requests"] += 1

        if event.get("success") is True:
            data["successes"] += 1
        else:
            data["failures"] += 1

        latency = event.get(
            "latency_ms"
        )

        if isinstance(
            latency,
            (int, float)
        ):
            data["latencies"].append(
                latency
            )

        if event.get(
            "metadata",
            {}
        ).get("route_match") is False:
            data["route_mismatches"] += 1

    route_metrics = {}

    for route, data in by_route.items():

        requests = data["requests"]

        route_metrics[route] = {
            "requests": requests,
            "successes": data["successes"],
            "failures": data["failures"],
            "success_rate": round(
                (
                    data["successes"]
                    / requests
                    * 100
                )
                if requests
                else 0.0,
                2,
            ),
            "average_latency_ms": round(
                (
                    sum(data["latencies"])
                    / len(data["latencies"])
                )
                if data["latencies"]
                else 0.0,
                2,
            ),
            "route_mismatches": data[
                "route_mismatches"
            ],
        }

    return {
        "total_requests": total,
        "successful_requests": successful,
        "failed_requests": failed,
        "success_rate": round(
            (
                successful / total * 100
            )
            if total
            else 0.0,
            2,
        ),
        "average_latency_ms": average_latency,
        "route_mismatches": mismatches,
        "by_route": route_metrics,
    }