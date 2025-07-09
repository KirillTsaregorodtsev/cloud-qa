import logging

from api.gpu_cluster import send_gpu_cluster_create_request
from task_manager.task_manager import wait_for_task_sync

logger = logging.getLogger(__name__)


def create_one_gpu_cluster(cluster_id: int) -> None:
    """
    Creates a GPU cluster with the specified cluster ID.

    Args:
        cluster_id (int): Unique identifier for the GPU cluster.

    Raises:
        ValueError: If the creation of the GPU cluster fails.
    """

    try:
        task_ids = send_gpu_cluster_create_request(cluster_id)
        task = wait_for_task_sync(task_ids.tasks[0], sleep_sec=10)
        instance_id = task.id
        logger.info(f"GPU cluster {cluster_id} created with Cluster ID {instance_id}")
    except Exception as e:
        logger.error(f"Failed to create GPU cluster {cluster_id}: {e}")
        raise ValueError(f"Failed to create GPU cluster {cluster_id}: {e}")