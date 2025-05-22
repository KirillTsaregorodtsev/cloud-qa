import logging

from gcore.types.cloud import QuotaGetByRegionResponse

from . import client

logger = logging.getLogger(__name__)


def get_regional_quotas(client_id, region_id) -> QuotaGetByRegionResponse | None:
    try:
        response = client.cloud.quotas.get_by_region(client_id=client_id, region_id=region_id)
        return response
    except Exception as e:
        logger.error(f"Failed to get quota for client {client_id} in region {region_id}: {e}")
        return None