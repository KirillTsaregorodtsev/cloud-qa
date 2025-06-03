from src.api.baremetal import get_baremetal_list
from src.config.settings import LOG_FILE, FLAVOR
from src.tasks.teardown_task import cleanup_region
from src.utils.logger import setup_logger
from src.worker_pool.worker_pool import WorkerPool


def main():
    """
    Main function to run server cleanup tasks.

    This function creates a worker pool and tasks to delete baremetal instances
    of a given flavor. It logs the number of servers to be deleted and their
    flavor ID.

    """
    logger = setup_logger("server_creator", log_file=LOG_FILE)


    # Initialize pool
    worker_pool = WorkerPool(max_workers=5)

    # List of server IDs
    bm_count, ids = get_baremetal_list(flavor_id=FLAVOR)
    logger.info(f"Count:  {bm_count} servers will be deleted. Flavor: {FLAVOR}")
    # Execute tasks
    worker_pool.execute(lambda x: cleanup_region(instance_id=x), ids)

if __name__ == "__main__":
    main()