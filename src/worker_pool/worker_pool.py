import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Iterable, Any, Union




class TaskError:
    """
    Представляет ошибку, возникшую при выполнении задачи.
    """
    def __init__(self, item: Any, exception: Exception):
        self.item = item
        self.exception = exception

    def __repr__(self) -> str:
        return f"<TaskError item={self.item!r} exception={self.exception!r}>"

class WorkerPool:
    def __init__(self, max_workers: int):
        """
        Инициализирует пул рабочих потоков.
        :param max_workers: Максимальное количество потоков.
        """
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)

    def execute(self, task: Callable[[Any], None], items: Iterable[Any]) -> None:
        """
        Выполняет задачи без возврата результата, с логгированием ошибок.
        """
        def safe_task(item: Any) -> None:
            try:
                task(item)
            except Exception as e:
                self.logger.error(f"Ошибка при обработке элемента {item}: {e}")

        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                executor.map(safe_task, items)
        except KeyboardInterrupt:
            self.logger.warning("Выполнение было прервано пользователем.")
            raise

    def execute_with_results(self, task: Callable[[Any], Any], items: Iterable[Any]) -> list[Union[Any, TaskError]]:
        """
        Выполняет задачи с возвратом результатов, включая ошибки как TaskError.
        """
        def safe_task(item: Any) -> Union[Any, TaskError]:
            try:
                return task(item)
            except Exception as e:
                self.logger.error(f"Ошибка при обработке элемента {item}: {e}")
                return TaskError(item, e)

        try:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                return list(executor.map(safe_task, items))
        except KeyboardInterrupt:
            self.logger.warning("Выполнение было прервано пользователем.")
            raise