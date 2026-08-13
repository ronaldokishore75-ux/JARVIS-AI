# =========================================================
# JARVIS V5 - SMART TASK ENGINE
# =========================================================

import re


def normalize_command(command):

    command = command.lower().strip()

    # Whisper sometimes gives us punctuation
    command = re.sub(
        r"[,.!?;:]+",
        " ",
        command
    )

    # Remove repeated spaces
    command = re.sub(
        r"\s+",
        " ",
        command
    )

    return command.strip()


def split_task(command):
    """
    Split a spoken multi-step command into task steps.

    Handles:
        and
        then
        after that
        commas

    Also tolerates some Whisper variations such as:
        "open youtube scroll down"
        "open youtube scroll and scroll down"
    """

    command = normalize_command(command)

    if not command:
        return []

    # -----------------------------------------------------
    # Normalize common task connectors
    # -----------------------------------------------------

    command = re.sub(
        r"\s+after that\s+",
        " and ",
        command
    )

    command = re.sub(
        r"\s+then\s+",
        " and ",
        command
    )

    command = re.sub(
        r"\s*,\s*",
        " and ",
        command
    )

    # -----------------------------------------------------
    # Split on "and"
    # -----------------------------------------------------

    parts = [
        part.strip()
        for part in command.split(" and ")
        if part.strip()
    ]

    # -----------------------------------------------------
    # Repair common Whisper phrasing:
    #
    # "open youtube scroll"
    # "open youtube scroll down"
    #
    # We only repair known action words so normal search
    # phrases aren't randomly split.
    # -----------------------------------------------------

    action_starters = [
        "open ",
        "search ",
        "scroll ",
        "click ",
        "go ",
        "press ",
        "move ",
        "play",
        "pause",
        "close ",
        "refresh",
        "mute",
        "unmute",
        "skip ",
        "find ",
    ]

    repaired_parts = []

    for part in parts:

        # Try to find a second known action inside the same part
        positions = []

        for starter in action_starters:

            start = 0

            while True:

                position = part.find(
                    starter,
                    start
                )

                if position == -1:
                    break

                if position > 0:

                    positions.append(
                        position
                    )

                start = position + 1

        # No internal action boundary
        if not positions:

            repaired_parts.append(part)
            continue

        # Split at the first internal action boundary
        split_position = min(positions)

        first = part[:split_position].strip()
        second = part[split_position:].strip()

        if first:
            repaired_parts.append(first)

        if second:
            repaired_parts.append(second)

    # -----------------------------------------------------
    # Repair repeated "scroll" speech
    #
    # "scroll and scroll down"
    #
    # After normalization this may become:
    # "scroll"
    # "scroll down"
    #
    # Keep both as valid steps.
    # -----------------------------------------------------

    final_parts = []

    for part in repaired_parts:

        part = part.strip()

        if not part:
            continue

        final_parts.append(part)

    return final_parts