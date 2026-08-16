# =========================================================
# JARVIS V8.6.1 - OBSERVABILITY LOGGER
# =========================================================

import json
import os
import time
from datetime import datetime


OBSERVABILITY_FILE = "observability.jsonl"


# =========================================================
# TIMESTAMP
# =========================================================

def current_timestamp():

    return datetime.now().isoformat(
        timespec="seconds"
    )


# =========================================================
# CREATE EVENT
# =========================================================

def create_event(
    command,
    route,
    success,
    latency_ms=None,
    error=None,
    metadata=None,
):
    """
    Build one structured JARVIS observability event.
    """

    return {
        "timestamp": current_timestamp(),
        "command": command,
        "route": route,
        "success": bool(success),
        "latency_ms": latency_ms,
        "error": error,
        "metadata": metadata or {},
    }


# =========================================================
# WRITE EVENT
# =========================================================

def log_event(
    event,
    filepath=OBSERVABILITY_FILE,
):

    directory = os.path.dirname(
        os.path.abspath(filepath)
    )

    os.makedirs(
        directory,
        exist_ok=True
    )

    with open(
        filepath,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(
                event,
                ensure_ascii=False
            )
            + "\n"
        )


# =========================================================
# TIMED OPERATION
# =========================================================

def elapsed_ms(
    start_time,
):

    return round(
        (time.perf_counter() - start_time)
        * 1000,
        2,
    )