import logging

from src.api.task import get_task_status
from gcore.types.cloud import Task
from time import sleep

logger = logging.getLogger(__name__)


def wait_for_task_sync(task_id: str, desired_state="FINISHED", timeout=2400, sleep_sec=3) -> Task:
    # By default, wait 180+ seconds for task to complete
    for _ in range(0, timeout, sleep_sec):
        try:
            task = get_task_status(task_id)
        except Exception:
            logger.exception(f"Failed to get task {task_id}")
            sleep(sleep_sec)
            continue
        if task.state in ("NEW", "RUNNING"):
            sleep(sleep_sec)
            continue
        logger.info(f"Task is: {task}")
        if task.state != desired_state:
            error_text = f"Task {task.task_type} {task.id} is in {task.state} state. Error: {task.error}."
            raise AssertionError(error_text)
        return task
    raise TimeoutError