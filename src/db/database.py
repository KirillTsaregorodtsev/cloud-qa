import logging
import sqlite3
import os
from typing import Dict, Optional
from src.config.settings import DB_FILE, DB_INIT_SQL, get_project_root

logger = logging.getLogger(__name__)


class Database:
    """Class for managing SQLite database operations."""

    def __init__(self, db_file: str = DB_FILE, clear_on_init: bool = False,
                 connection: Optional[sqlite3.Connection] = None):
        self.db_file = os.path.join(get_project_root(), db_file)
        self.connection = connection
        self._initialize_database(clear_on_init)
        logger.debug(f"Database initialized at: {self.db_file}")

    def _initialize_database(self, clear_on_init: bool) -> None:
        """Initializes the database using an SQL script."""
        try:
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
            sql_file = os.path.join(get_project_root(), DB_INIT_SQL)
            logger.debug(f"Reading SQL initialization script from: {sql_file}")

            if not os.path.exists(sql_file):
                logger.error(f"SQL initialization file not found: {sql_file}")
                raise FileNotFoundError(f"SQL file {sql_file} does not exist")

            with self._get_connection() as conn:
                cursor = conn.cursor()

                if clear_on_init:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    for table in tables:
                        cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
                        logger.info(f"Dropped table {table[0]}")

                with open(sql_file, "r", encoding="utf-8") as f:
                    sql_script = f.read()
                cursor.executescript(sql_script)
                conn.commit()
                logger.info("Database initialized with SQL script")
        except (sqlite3.Error, FileNotFoundError) as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    def _get_connection(self) -> sqlite3.Connection:
        """Returns the existing connection or creates a new one."""
        if self.connection is not None:
            return self.connection
        # Устанавливаем таймаут 10 секунд для предотвращения ошибки "database is locked"
        return sqlite3.connect(self.db_file, timeout=10.0)

    def save_baremetal_data(self, hostname: str, node_id: str) -> None:
        """Saves baremetal configuration data to the database."""
        try:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO servers (
                        hostname, node_id
                    ) VALUES (?, ?)
                """, (
                    hostname,
                    node_id
                ))
                conn.commit()
                logger.info(f"Saved baremetal {node_id} data to database")
        except sqlite3.Error as e:
            logger.error(f"Failed to save baremetal {node_id} data: {e}")
            raise e