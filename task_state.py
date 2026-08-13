# =========================================================
# JARVIS V5.3 - TASK STATE
# =========================================================

from dataclasses import dataclass, asdict
from threading import Lock
from typing import Optional


@dataclass
class TaskState:

    goal: str = ""

    status: str = "IDLE"

    current_step: int = 0

    total_steps: int = 0

    current_action: str = ""

    current_value: Optional[object] = None

    last_result: Optional[object] = None

    error: Optional[str] = None


class TaskStateManager:

    def __init__(self):

        self._state = TaskState()

        self._lock = Lock()


    # =====================================================
    # START TASK
    # =====================================================

    def start(
        self,
        goal,
        total_steps
    ):

        with self._lock:

            self._state = TaskState(

                goal=goal,

                status="RUNNING",

                current_step=0,

                total_steps=total_steps,

                current_action="",

                current_value=None,

                last_result=None,

                error=None
            )


    # =====================================================
    # START STEP
    # =====================================================

    def start_step(
        self,
        step_number,
        action,
        value=None
    ):

        with self._lock:

            self._state.current_step = step_number

            self._state.current_action = action

            self._state.current_value = value

            self._state.last_result = None


    # =====================================================
    # STEP SUCCESS
    # =====================================================

    def step_completed(self, result=None):

        with self._lock:

            self._state.last_result = result


    # =====================================================
    # COMPLETE TASK
    # =====================================================

    def complete(self):

        with self._lock:

            self._state.status = "COMPLETED"


    # =====================================================
    # CANCEL TASK
    # =====================================================

    def cancel(self):

        with self._lock:

            self._state.status = "CANCELLED"


    # =====================================================
    # FAIL TASK
    # =====================================================

    def fail(self, error):

        with self._lock:

            self._state.status = "FAILED"

            self._state.error = str(error)


    # =====================================================
    # RESET
    # =====================================================

    def reset(self):

        with self._lock:

            self._state = TaskState()


    # =====================================================
    # GET STATE
    # =====================================================

    def get_state(self):

        with self._lock:

            return asdict(
                self._state
            )


# =========================================================
# ONE SHARED STATE MANAGER
# =========================================================

task_state = TaskStateManager()