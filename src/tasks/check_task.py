from src.tasks.server_tasks import check_server
from src.worker_pool.types import ServerInfo


def task(info: ServerInfo):
    check_server(server_id=info.server_id, instance_id=info.instance_id, ip_address=info.ip_address)