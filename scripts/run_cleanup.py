from src.config.settings import LOG_FILE
from src.utils.logger import setup_logger
from src.worker_pool.worker_pool import WorkerPool


def main():
    logger = setup_logger("server_creator", log_file=LOG_FILE)


    # Initialize pool
    worker_pool = WorkerPool(max_workers=5)

    # List of server IDs
    ids = list(range(OFFSET + 1, NUMBER_OF_SERVERS + 1))
    logger.info(f"Creating {len(ids)} servers")
    # Execute tasks
    worker_pool.execute(lambda x: create_one_server(x), ids)

if __name__ == "__main__":
    main()