# =========================================================
# JARVIS V5 - TASK RUNNER
# =========================================================

import time
import threading

from task_state import task_state
from planner import create_plan
from verifier import verify_step
from goal_verifier import verify_goal


# =========================================================
# LIVE CANCELLATION
# =========================================================

cancel_event = threading.Event()


def request_task_cancel():

    cancel_event.set()

    print(
        "V5 TASK: Live cancellation requested."
    )


def reset_task_cancel():

    cancel_event.clear()


def is_task_cancelled():

    return cancel_event.is_set()


# =========================================================
# RUN STRUCTURED PLAN
# =========================================================

def run_task(
    command,
    execute_step,
    progress_callback=None
):

    reset_task_cancel()

    plan = create_plan(command)

    # =====================================================
    # NO PLAN
    # =====================================================

    if not plan.steps:

        print(
            "V5 TASK: Planner produced no steps."
        )

        task_state.fail(
            "Planner produced no steps."
        )

        return [
            "I couldn't create a plan for that task."
        ]


    results = []

    total_steps = len(plan.steps)

    print(
        f"V5 PLAN: {total_steps} steps"
    )


    # =====================================================
    # INITIALIZE TASK STATE
    # =====================================================

    task_state.start(
        command,
        total_steps
    )


    try:

        # =================================================
        # RUN EACH STEP
        # =================================================

        for number, step in enumerate(
            plan.steps,
            start=1
        ):

            # =============================================
            # CANCELLATION CHECK
            # =============================================

            if is_task_cancelled():

                print(
                    f"V5 TASK: Cancelled before "
                    f"step {number}."
                )

                task_state.cancel()

                if progress_callback:

                    progress_callback(
                        "cancelled",
                        number,
                        total_steps,
                        "Task cancelled"
                    )

                results.append(
                    "Task cancelled."
                )

                break


            # =============================================
            # UPDATE CURRENT STEP
            # =============================================

            task_state.start_step(
                number,
                step.action,
                step.value
            )

            if progress_callback:

                progress_callback(
                    "step_started",
                    number,
                    total_steps,
                    step.description
                )


            print(
                f"V5 STEP {number}/{total_steps}: "
                f"{step.description}"
            )

            print(
                f"V5 ACTION: {step.action}"
            )

            print(
                f"V5 VALUE: {step.value}"
            )


            # =============================================
            # EXECUTE STEP
            # =============================================

            try:

                result = execute_step(
                    step.action,
                    step.value
                )

                # =========================================
                # STEP VERIFICATION
                # =========================================

                verified = verify_step(
                    step.action,
                    step.value,
                    result
                )

                print(
                    f"V5 VERIFY: "
                    f"{step.action} -> {verified}"
                )

                if not verified:

                    print(
                        f"V5 VERIFY FAILED: "
                        f"{step.description}"
                    )

                    result = None


            except Exception as error:

                print(
                    f"V5 TASK ERROR: {error}"
                )

                result = None


            # =============================================
            # DETECT FAILURE
            # =============================================

            failed = (
                result is False
                or result is None
                or (
                    isinstance(result, str)
                    and (
                        "couldn't" in result.lower()
                        or "failed" in result.lower()
                        or "error" in result.lower()
                        or "not found" in result.lower()
                    )
                )
            )


            # =============================================
            # RETRY / RECOVERY
            # =============================================

            if failed:

                print(
                    f"V5 STEP {number} failed."
                )

                recovered = False


                # -----------------------------------------
                # CLICK RECOVERY
                # -----------------------------------------

                if step.action == "click_link":

                    print(
                        "V5 RECOVERY: "
                        "Scrolling once and retrying click..."
                    )

                    if not is_task_cancelled():

                        try:

                            execute_step(
                                "scroll_down",
                                None
                            )

                            time.sleep(1)

                            retry_result = execute_step(
                                step.action,
                                step.value
                            )

                            retry_verified = verify_step(
                                step.action,
                                step.value,
                                retry_result
                            )

                            print(
                                f"V5 VERIFY RETRY: "
                                f"{step.action} "
                                f"-> {retry_verified}"
                            )

                            recovered = retry_verified

                            if recovered:

                                result = retry_result

                        except Exception as error:

                            print(
                                f"V5 RECOVERY ERROR: {error}"
                            )


                # -----------------------------------------
                # GENERIC RETRY
                # -----------------------------------------

                if not recovered:

                    print(
                        "V5 RECOVERY: "
                        "Retrying step once..."
                    )

                    if not is_task_cancelled():

                        time.sleep(1)

                        try:

                            retry_result = execute_step(
                                step.action,
                                step.value
                            )

                            retry_verified = verify_step(
                                step.action,
                                step.value,
                                retry_result
                            )

                            print(
                                f"V5 VERIFY RETRY: "
                                f"{step.action} "
                                f"-> {retry_verified}"
                            )

                            recovered = retry_verified

                            if recovered:

                                result = retry_result

                        except Exception as error:

                            print(
                                f"V5 RETRY ERROR: {error}"
                            )


                # -----------------------------------------
                # FINAL FAILURE
                # -----------------------------------------

                if not recovered:

                    error_message = (
                        f"Step {number} failed."
                    )

                    print(
                        f"V5 TASK: Step {number} "
                        "could not be completed."
                    )

                    task_state.fail(
                        error_message
                    )

                    if progress_callback:

                        progress_callback(
                            "failed",
                            number,
                            total_steps,
                            error_message
                        )

                    results.append(
                        error_message
                    )

                    break


            # =============================================
            # STEP SUCCESS
            # =============================================

            task_state.step_completed(
                result
            )

            results.append(
                result
            )

            if progress_callback:

                progress_callback(
                    "step_completed",
                    number,
                    total_steps,
                    step.description
                )


            # =============================================
            # CANCELLATION WINDOW
            # =============================================

            time.sleep(1.0)


        else:

            # =================================================
            # ALL STEPS FINISHED
            # =================================================

            goal_verified = verify_goal(
                command,
                results
            )

            print(
                f"V5 GOAL VERIFY: {goal_verified}"
            )


            # =============================================
            # GOAL SUCCESS
            # =============================================

            if goal_verified:

                task_state.complete()

                if progress_callback:

                    progress_callback(
                        "completed",
                        total_steps,
                        total_steps,
                        "Task completed"
                    )


            # =============================================
            # GOAL FAILURE
            # =============================================

            else:

                error_message = (
                    "The task steps completed, "
                    "but the overall goal was not verified."
                )

                print(
                    f"V5 GOAL VERIFY FAILED: "
                    f"{error_message}"
                )

                task_state.fail(
                    error_message
                )

                if progress_callback:

                    progress_callback(
                        "failed",
                        total_steps,
                        total_steps,
                        error_message
                    )

                results.append(
                    error_message
                )


    # =====================================================
    # UNEXPECTED TASK ERROR
    # =====================================================

    except Exception as error:

        error_message = (
            f"Task failed: {error}"
        )

        print(
            f"V5 TASK ERROR: {error}"
        )

        task_state.fail(
            str(error)
        )

        state = task_state.get_state()

        if progress_callback:

            progress_callback(
                "failed",
                state["current_step"],
                total_steps,
                error_message
            )

        results.append(
            error_message
        )


    return results