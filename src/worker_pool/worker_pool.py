import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, Any, Union




class TaskError:
    """
    Represents an error that occurred while performing a task.
    """
    def __init__(self, item: Any, exception: Exception):
        self.item = item
        self.exception = exception

    def __repr__(self) -> str:
        return f"<TaskError item={self.item!r} exception={self.exception!r}>"

class WorkerPool:
    def __init__(self, max_workers: int):
        """
        Initializes the pool of worker threads.
        :param max_workers: Maximum number of threads.
        """
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)

    def execute(self, task: Callable[[Any], None], items: Iterable[Any]) -> None:
        """
        Executes tasks without returning a result, with error logging.
        """
        def safe_task(item: Any) -> None:
            try:
                task(item)
            except Exception as e:
                self.logger.error(f"Error during item processing {item}: {e}")

        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                executor.map(safe_task, items)
        except KeyboardInterrupt:
            self.logger.warning("The execution was interrupted by the user.")
            raise

    def execute_with_results(self, task: Callable[[Any], Any], items: Iterable[Any]) -> list[Union[Any, TaskError]]:
        """
        Executes tasks with results returned, including errors as TaskError.
        """
        def safe_task(item: Any) -> Union[Any, TaskError]:
            try:
                return task(item)
            except Exception as e:
                self.logger.error(f"Error during item processing {item}: {e}")
                return TaskError(item, e)

        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                return list(executor.map(safe_task, items))
        except KeyboardInterrupt:
            self.logger.warning("The execution was interrupted by the user.")
            raise