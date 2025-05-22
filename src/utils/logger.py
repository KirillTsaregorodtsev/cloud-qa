import logging
import os
from typing import Optional
from src.config.settings import PROJECT_ROOT

_LOGGER_INITIALIZED = False

def setup_logger(name: str = __name__, log_file: Optional[str] = None) -> logging.Logger:
    """
    Sets up logging configuration for the application.

    Args:
        name: Name of the logger (usually __name__ of the module).
        log_file: Path to the log file relative to project root. If None, logs to console only.

    Returns:
        Configured logger instance for the specified name.
    """
    global _LOGGER_INITIALIZED
    logger = logging.getLogger(name)

    if _LOGGER_INITIALIZED:
        logger.debug(f"Logger {name} requested, but logging already initialized")
        return logger

    root_logger = logging.getLogger('')
    root_logger.setLevel(logging.DEBUG)
    logger.debug("Configuring root logger")

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    logger.debug("Console handler added")

    if log_file:
        try:
            project_root = PROJECT_ROOT
            absolute_log_file = os.path.join(project_root, log_file)
            log_dir = os.path.dirname(absolute_log_file)
            logger.debug(f"Ensuring log directory exists: {log_dir}")
            os.makedirs(log_dir, exist_ok=True)
            logger.debug(f"Creating FileHandler for: {absolute_log_file}")
            file_handler = logging.FileHandler(absolute_log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            logger.debug(f"FileHandler added for: {absolute_log_file}")
        except Exception as e:
            logger.error(f"Failed to create FileHandler for {absolute_log_file}: {e}")
            raise

    _LOGGER_INITIALIZED = True
    logger.info("Logger initialized successfully")
    return logger