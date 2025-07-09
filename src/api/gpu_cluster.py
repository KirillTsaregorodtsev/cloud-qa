import logging
from typing import Any
from gcore.types.cloud import TaskIDList


from src.config.settings import JIRA_TASK_ID, SSH_KEY_NAME, FLAVOR, INSTANCES_COUNT
from . import client

logger = logging.getLogger(__name__)

def get_gpu_cluster_list() -> Any:
    return client.cloud.gpu_baremetal_clusters.list()


def get_cluster_image_id(image_name: str) -> str:
    logger.info(f"Getting image ID for {image_name}")
    images = client.cloud.gpu_baremetal_clusters.images.list()
    for image in images.results:
        if image.name == image_name:
            logger.info(f"Found image {image_name} with ID {image.id}")
            return image.id
    raise ValueError(f"Image {image_name} not found")


def send_gpu_cluster_create_request(i: int) -> TaskIDList:
    jira_task_id = JIRA_TASK_ID
    project_id = client.cloud_project_id
    region_id = client.cloud_region_id
    flavor = FLAVOR
    instances_count = INSTANCES_COUNT
    image_id = get_cluster_image_id(image_name="ubuntu-22.04-x64-nvidia-a100")
    interfaces = [{"type": "external"}]
    instance_name = f"qa_autotest_gpu_bm_{jira_task_id}_tk_{i}"
    logger.info(f"Creating baremetal instance {instance_name} in {project_id}/{region_id}")
    return client.cloud.gpu_baremetal_clusters.create(
        name=instance_name,
        instances_count= instances_count,
        image_id=image_id,
        flavor=flavor,
        ssh_key_name=SSH_KEY_NAME,
        interfaces=interfaces)