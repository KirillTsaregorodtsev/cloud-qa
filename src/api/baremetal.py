import logging
from typing import Any

from gcore.types.cloud import TaskIDList, BaremetalFlavorList, Instance

from src.config.settings import JIRA_TASK_ID, SSH_KEY_NAME, FLAVOR
from . import client

logger = logging.getLogger(__name__)


def get_image_id(image_name: str) -> str:
    logger.info(f"Getting image ID for {image_name}")
    images = client.cloud.baremetal.images.list()
    for image in images.results:
        if image.name == image_name:
            logger.info(f"Found image {image_name} with ID {image.id}")
            return image.id
    raise ValueError(f"Image {image_name} not found")

def send_baremetal_create_request(i: int) -> TaskIDList:
    jira_task_id = JIRA_TASK_ID
    project_id = client.cloud_project_id
    region_id = client.cloud_region_id
    flavor = FLAVOR
    image_id = get_image_id(image_name="ubuntu-22.04-x64-ironic")
    interfaces = [{"type": "external"}]
    instance_name = f"qa_autotest_bm_{jira_task_id}_tk_{i}"
    logger.info(f"Creating baremetal instance {instance_name} in {project_id}/{region_id}")
    return client.cloud.baremetal.servers.create(
        name=instance_name,
        image_id=image_id,
        flavor=flavor,
        ssh_key_name=SSH_KEY_NAME,
        interfaces=interfaces)

def get_instance_ip_address(instance_id: str):
    logger.info(f"Getting IP address for {instance_id}")
    try:
        instance = client.cloud.instances.get(
            instance_id=instance_id
        )
        return instance.addresses['pub_net'][0].addr
    except Exception as e:
        logger.error(f"Failed to get IP address for {instance_id}: {e}")
        raise ValueError(f"Failed to get IP address for {instance_id}: {e}")

def get_baremetal_flavors(region_id=client.cloud_region_id) -> BaremetalFlavorList:
    logger.info("Getting baremetal flavors")
    return client.cloud.baremetal.flavors.list(project_id=client.cloud_project_id, region_id=region_id, include_capacity=True)

def get_baremetal_overview(instance_id: str) -> Instance:
    logger.info(f"Getting baremetal overview for {instance_id}")
    return client.cloud.instances.get(instance_id=instance_id)

def delete_baremetal_instance(instance_id: str) -> TaskIDList:
    logger.info(f"Deleting baremetal instance {instance_id}")
    try:
        return client.cloud.instances.delete(instance_id=instance_id)
    except Exception as e:
        logger.error(f"Failed to delete baremetal instance {instance_id}: {e}")
        raise ValueError(f"Failed to delete baremetal instance {instance_id}: {e}")

def get_baremetal_list(flavor_id:str) -> tuple[int, list[str]]:
    logger.info("Getting baremetal list")
    result = []
    try:
        bm_list = client.cloud.baremetal.servers.list(flavor_id=flavor_id)
        for bm in bm_list.results:
            result.append(bm.id)
        return bm_list.count, result
    except Exception as e:
        logger.error(f"Failed to get baremetal list: {e}")
        raise ValueError(f"Failed to get baremetal list: {e}")