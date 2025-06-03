from src.api.baremetal import get_baremetal_list, get_instance_ip_address
from src.config.settings import LOG_FILE, FLAVOR
from src.report.csv_reporter import CSVReporter
from src.tasks.check_task import task
from src.utils.logger import setup_logger
from src.worker_pool.types import ServerInfo
from src.worker_pool.worker_pool import WorkerPool


def main():
    logger = setup_logger("server_creator", log_file=LOG_FILE)
    ips = []


    # Initialize pool
    worker_pool = WorkerPool(max_workers=5)

    # List of server IDs
    bm_count, ids = get_baremetal_list(flavor_id=FLAVOR)

    for item in ids:
        ip = get_instance_ip_address(instance_id=item)
        ips.append(ip)

    items = [ServerInfo(i, sid, ip) for i, (sid, ip) in enumerate(zip(ids, ips))]
    # Execute tasks
    worker_pool.execute(task, items)

    # CSV report will be handled separately
    logger.info("Server creation tasks completed. JSON files saved in tmp/.")
    reporter = CSVReporter()
    reporter.write_report()

    logger.info("Server creation and reporting completed.")

if __name__ == "__main__":
    main()