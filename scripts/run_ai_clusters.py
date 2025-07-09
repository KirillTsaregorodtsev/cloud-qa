from config.settings import LOG_FILE, MAX_WORKERS, OFFSET, NUMBER_OF_SERVERS
from src.utils.logger import setup_logger
from tasks.gpu_tasks import create_one_gpu_cluster
from worker_pool.worker_pool import WorkerPool


def main():
    logger = setup_logger("server_cleanup", log_file=LOG_FILE)

    # Initialize pool
    worker_pool = WorkerPool(max_workers=int(MAX_WORKERS))

    # List of server IDs
    ids = list(range(OFFSET + 1, NUMBER_OF_SERVERS + 1))
    logger.info(f"Creating {len(ids)} servers")

    # Execute tasks
    worker_pool.execute(lambda x: create_one_gpu_cluster(x), ids)

if __name__ == "__main__":
    main()