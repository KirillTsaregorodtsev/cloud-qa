import logging
from src.api.baremetal import delete_baremetal_instance
from src.task_manager.task_manager import wait_for_task_sync

logger = logging.getLogger(__name__)


def cleanup_region(instance_id: str):

    """
    Cleans up a specified baremetal instance by deleting it.

    Args:
        instance_id (str): The ID of the instance to be deleted.

    Raises:
        ValueError: If the instance deletion fails.
    """
    task_status = None
    task = None
    try:
        task_ids = delete_baremetal_instance(instance_id=instance_id)
        task = wait_for_task_sync(task_ids.tasks[0], sleep_sec=10)
        task_status = task.state
    except Exception as e:
        logger.error(f"Failed to delete instance {instance_id}, task id: {task}; task status: {task_status}: {e}")
        raise ValueError(f"Failed to delete instance {instance_id}: {e}")