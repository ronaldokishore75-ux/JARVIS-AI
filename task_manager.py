import threading
from task_runner import run_task

_task_thread=None
_task_running=None



def start_task(command, execute_step, progress_callback=None):

    global _task_thread
    global _task_running

    if _task_running:

        print("V5 TASK: A task is already running.")

        return False

    _task_running = True

    def worker():

        global _task_running

        try:

            results = run_task(
                command,
                execute_step,
                progress_callback
            )

            print("V5 TASK RESULTS:")

            for result in results:
                print(result)

        except Exception as error:

            print(
                f"V5 TASK ERROR: {error}"
            )

        finally:

            _task_running = False

            print(
                "V5 TASK: Finished."
            )

    _task_thread = threading.Thread(
        target=worker,
        daemon=True
    )

    _task_thread.start()

    return True