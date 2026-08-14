# =========================================================
# JARVIS V5 - TASK PLANNER
# =========================================================

from dataclasses import dataclass, field
from typing import List
import re


# =========================================================
# TASK DATA STRUCTURES
# =========================================================

@dataclass
class TaskStep:

    action: str
    value: object = None
    description: str = ""


@dataclass
class TaskPlan:

    goal: str
    steps: List[TaskStep] = field(
        default_factory=list
    )


# =========================================================
# CREATE PLAN
# =========================================================

def create_plan(command):
    """
    Convert a user goal into a structured V5 plan.

    This version is rule-based and handles common
    YouTube multi-step commands.
    """

    command = command.lower().strip()

    if not command:

        return TaskPlan(
            goal="",
            steps=[]
        )

    steps = []

    # =====================================================
    # YOUTUBE TASKS
    # =====================================================

    if "youtube" in command:

        # -------------------------------------------------
        # STEP 1 - OPEN YOUTUBE
        # -------------------------------------------------

        steps.append(
            TaskStep(
                action="open_youtube",
                value=None,
                description="Open YouTube"
            )
        )


        # -------------------------------------------------
        # STEP 2 - SEARCH YOUTUBE
        # -------------------------------------------------

        query = extract_youtube_query(
            command
        )

        if query:

            steps.append(
                TaskStep(
                    action="search_youtube",
                    value=query,
                    description=(
                        f'Search YouTube for "{query}"'
                    )
                )
            )


        # -------------------------------------------------
        # STEP 3 - SCROLL
        # -------------------------------------------------

        scroll_count = count_scrolls(
            command
        )

        for _ in range(
            scroll_count
        ):

            steps.append(
                TaskStep(
                    action="scroll_down",
                    value=None,
                    description="Scroll down"
                )
            )


        # -------------------------------------------------
        # STEP 4 - CLICK LINK
        # -------------------------------------------------

        click_target = extract_click_target(
            command
        )

        if click_target:

            steps.append(
                TaskStep(
                    action="click_link",
                    value=click_target,
                    description=(
                        f'Click "{click_target}"'
                    )
                )
            )


        # -------------------------------------------------
        # STEP 5 - SUBSCRIBE
        # -------------------------------------------------

        if "subscribe" in command:

            steps.append(
                TaskStep(
                    action="click_link",
                    value="subscribe",
                    description='Click "subscribe"'
                )
            )


        # -------------------------------------------------
        # RETURN YOUTUBE PLAN
        # -------------------------------------------------

        return TaskPlan(
            goal=command,
            steps=steps
        )


    # =====================================================
    # NO KNOWN PLAN
    # =====================================================

    return TaskPlan(
        goal=command,
        steps=[]
    )


# =========================================================
# EXTRACT YOUTUBE QUERY
# =========================================================

def extract_youtube_query(command):

    command = command.lower().strip()

    patterns = [
        # "search youtube for python tutorials"
        r"search\s+youtube\s+for\s+(.+)",

        # "search youtube python tutorials"
        r"search\s+youtube\s+(.+)",

        # "search for python tutorials on youtube"
        r"search\s+for\s+(.+?)\s+on\s+youtube",

        # "find python tutorials on youtube"
        r"find\s+(.+?)\s+on\s+youtube",

        # "open youtube and search for python tutorials"
        r"youtube\s+and\s+search\s+(?:for\s+)?(.+)",

        # "open youtube then search for python tutorials"
        r"youtube\s+then\s+search\s+(?:for\s+)?(.+)",
    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            command
        )

        if not match:
            continue


        query = match.group(
            1
        ).strip()


        # -------------------------------------------------
        # Remove trailing actions
        # -------------------------------------------------

        trailing_markers = [
            " and scroll",
            " scroll",
            " and click",
            " click",
            " and subscribe",
            " subscribe",
        ]


        for marker in trailing_markers:

            if marker in query:

                query = query.split(
                    marker,
                    1
                )[0].strip()


        # -------------------------------------------------
        # Remove trailing punctuation
        # -------------------------------------------------

        query = query.rstrip(
            " .,!?-"
        ).strip()


        if query:

            return query


    return None


# =========================================================
# COUNT SCROLL COMMANDS
# =========================================================

def count_scrolls(command):

    count = command.count(
        "scroll down"
    )


    # -----------------------------------------------------
    # Handle "scroll" by itself
    # -----------------------------------------------------

    if (
        count == 0
        and "scroll" in command
    ):

        count = 1


    return count


# =========================================================
# EXTRACT CLICK TARGET
# =========================================================

def extract_click_target(command):

    # -----------------------------------------------------
    # "click python course"
    # -----------------------------------------------------

    match = re.search(
        r"\bclick\s+(.+)",
        command
    )

    if match:

        target = match.group(
            1
        ).strip()

    else:

        target = None


    if not target:

        return None


    # -----------------------------------------------------
    # Remove trailing task actions
    # -----------------------------------------------------

    for marker in [
        " and scroll",
        " scroll",
        " and click",
        " click",
        " and subscribe",
        " subscribe",
    ]:

        if marker in target:

            target = target.split(
                marker,
                1
            )[0].strip()


    target = target.rstrip(
        " .,!?-"
    ).strip()


    return target or None