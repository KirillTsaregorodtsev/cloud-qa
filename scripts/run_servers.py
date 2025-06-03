import os
import shutil

from src.infrastructure.quotas_checks import check_quotas
from src.report.csv_reporter import CSVReporter
from src.worker_pool.worker_pool import WorkerPool
from src.tasks.server_tasks import create_one_server
from src.config.settings import MAX_WORKERS, LOG_FILE, OFFSET, NUMBER_OF_SERVERS, TMP_PATH
from src.utils.logger import setup_logger


def main():
    logger = setup_logger("server_creator", log_file=LOG_FILE)

    if OFFSET > NUMBER_OF_SERVERS:
        logger.error(f"OFFSET: {OFFSET} must be less than NUMBER_OF_SERVERS: {NUMBER_OF_SERVERS}")
        raise ValueError("OFFSET must be less than NUMBER_OF_SERVERS")

    # Check quotas before creating servers
    check_quotas()

    # clean up old JSON files
    if os.path.exists(TMP_PATH):
        logger.info(f"Cleaning up from {TMP_PATH} old JSON files")
        shutil.rmtree(TMP_PATH)

    # Initialize pool
    worker_pool = WorkerPool(max_workers=int(MAX_WORKERS))

    # List of server IDs
    ids = list(range(OFFSET + 1, NUMBER_OF_SERVERS + 1))
    logger.info(f"Creating {len(ids)} servers")
    # Execute tasks
    worker_pool.execute(lambda x: create_one_server(server_id=x), ids)

    # CSV report will be handled separately
    logger.info("Server creation tasks completed. JSON files saved in tmp/.")
    reporter = CSVReporter()
    reporter.write_report()

    logger.info("Server creation and reporting completed.")

if __name__ == "__main__":
    main()