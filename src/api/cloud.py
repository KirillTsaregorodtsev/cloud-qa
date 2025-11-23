import logging
from typing import Any

from src.api import client

logger = logging.getLogger(__name__)


def get_regions() -> Any:
    """
    Fetch region data from the GCore API.
    
    This function uses the initialized GCore client to retrieve
    available regions from the cloud API.
    
    Returns:
        Any: The result of gcore_api.cloud.regions() call
    """
    logger.info("Fetching regions from GCore API")
    try:
        # Using the client that's already initialized with proper credentials
        regions = client.cloud.regions.list()
        logger.info(f"Successfully fetched {len(regions.results) if hasattr(regions, 'results') else 'unknown'} regions")
        return regions
    except Exception as e:
        logger.error(f"Failed to fetch regions from GCore API: {e}")
        raise