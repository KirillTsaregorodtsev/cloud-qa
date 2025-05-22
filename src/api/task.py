import logging

from gcore.types.cloud import Task
from . import client

logger = logging.getLogger(__name__)


def get_task_status(task_id: str) -> Task:
    """
    Get task by ID
    :param task_id: Task ID
    :return: Task object
    """
    logger.info(f"Getting task status for {task_id}")
    task = client.cloud.tasks.get(task_id)
    return task