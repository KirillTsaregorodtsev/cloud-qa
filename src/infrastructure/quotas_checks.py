import logging

from src.api.quotas import get_regional_quotas
from src.config.settings import LOG_FILE, CLIENT_ID, REGION_ID, NUMBER_OF_SERVERS, OFFSET

logger = logging.getLogger(__name__)


def check_quotas():
    quotas = get_regional_quotas(client_id=CLIENT_ID, region_id=REGION_ID)

    assert quotas.baremetal_hf_count_limit - quotas.baremetal_hf_count_usage > (NUMBER_OF_SERVERS - OFFSET), \
        f"Insufficient baremetal_hf_count_usage: {quotas.baremetal_hf_count_usage} < {NUMBER_OF_SERVERS - OFFSET}"

    assert quotas.external_ip_count_limit - quotas.external_ip_count_usage > (NUMBER_OF_SERVERS - OFFSET), \
        f"Insufficient external_ip_count_usage: {quotas.external_ip_count_usage} < {NUMBER_OF_SERVERS - OFFSET}"

    assert quotas.baremetal_infrastructure_count_limit - quotas.baremetal_infrastructure_count_usage >= (NUMBER_OF_SERVERS - OFFSET), \
        f"Insufficient baremetal_infrastructure_count_usage: {quotas.baremetal_infrastructure_count_usage} < {NUMBER_OF_SERVERS - OFFSET}"