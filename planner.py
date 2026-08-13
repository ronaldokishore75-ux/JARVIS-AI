# =========================================================
# JARVIS V5 - TASK PLANNER
# =========================================================

from dataclasses import dataclass, field
from typing import List


@dataclass
class TaskStep:
    action: str
    value: object = None
    description: str = ""


@dataclass
class TaskPlan:
    goal: str
    steps: List[TaskStep] = field(default_factory=list)


def create_plan(command):
    """
    Convert a user goal into a structured V5 plan.

    This first version is rule-based.
    """

    command = command.lower().strip()

    if not command:
        return TaskPlan(
            goal="",
            steps=[]
        )

    steps = []

    # ---------------------------------------------------------
    # YOUTUBE TASKS
    # ---------------------------------------------------------

    if "youtube" in command:

        # Open YouTube
        steps.append(
            TaskStep(
                action="open_youtube",
                description="Open YouTube"
            )
        )

        # Search
        if "search" in command:

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

        # Scroll
        scroll_count = count_scrolls(command)

        for _ in range(scroll_count):

            steps.append(
                TaskStep(
                    action="scroll_down",
                    description="Scroll down"
                )
            )

        # Click
        if "click" in command:

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

    return TaskPlan(
        goal=command,
        steps=steps
    )


# =========================================================
# HELPERS
# =========================================================

def extract_youtube_query(command):

    patterns = [
        "search youtube for ",
        "search youtube ",
    ]

    for pattern in patterns:

        if pattern in command:

            query = command.split(
                pattern,
                1
            )[1].strip()

            # Remove trailing task actions
            for marker in [
                " and scroll",
                " scroll",
                " and click",
                " click",
            ]:

                if marker in query:

                    query = query.split(
                        marker,
                        1
                    )[0].strip()

            return query

    return None


def count_scrolls(command):

    count = command.count(
        "scroll down"
    )

    # Handle "scroll" by itself
    if count == 0 and "scroll" in command:

        count = 1

    return count


def extract_click_target(command):

    if "click " not in command:

        return None

    target = command.split(
        "click ",
        1
    )[1].strip()

    return target