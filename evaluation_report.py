# =========================================================
# JARVIS V8.7.1 - EVALUATION REPORT
# =========================================================

import json
from datetime import datetime


def build_evaluation_report(results):
    """
    Build a persistent, human-readable evaluation report.
    """

    total = len(results)

    passed = sum(
        1
        for result in results
        if result.passed
    )

    failed = total - passed

    score = (
        round(
            passed / total * 100,
            2,
        )
        if total
        else 0.0
    )

    route_counts = {}

    for result in results:

        route = "unknown"

        if result.passed:
            route = "pass"

        route_counts[route] = (
            route_counts.get(route, 0)
            + 1
        )

    lines = []

    lines.append(
        "=" * 60
    )

    lines.append(
        "JARVIS V8 EVALUATION REPORT"
    )

    lines.append(
        "=" * 60
    )

    lines.append(
        f"Timestamp: {datetime.now().isoformat(
            timespec='seconds'
        )}"
    )

    lines.append(
        f"Total cases: {total}"
    )

    lines.append(
        f"Passed:      {passed}"
    )

    lines.append(
        f"Failed:      {failed}"
    )

    lines.append(
        f"Score:       {score:.2f}%"
    )

    lines.append(
        ""
    )

    lines.append(
        "CASES:"
    )

    for result in results:

        status = (
            "PASS"
            if result.passed
            else "FAIL"
        )

        lines.append(
            f"  {result.name:<30} "
            f"{status}"
        )

    lines.append(
        ""
    )

    lines.append(
        "STATUS:"
    )

    if failed == 0:

        lines.append(
            "  JARVIS EVALUATION: PASS"
        )

    else:

        lines.append(
            "  JARVIS EVALUATION: NEEDS ATTENTION"
        )

    lines.append(
        "=" * 60
    )

    return "\n".join(lines)