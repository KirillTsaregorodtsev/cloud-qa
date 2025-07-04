PRAGMA foreign_keys = ON;

-- Таблица серверов
CREATE TABLE IF NOT EXISTS servers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname TEXT NOT NULL,
    node_id TEXT NOT NULL UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Таблица адресов сервера
CREATE TABLE IF NOT EXISTS server_ips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id INTEGER NOT NULL,
    ip_address TEXT NOT NULL,
    ip_version INTEGER DEFAULT 4,              -- 4 или 6
    interface TEXT,                            -- например, eth0, ib0
    role TEXT,                                 -- например, 'mgmt', 'storage', 'cluster'
    FOREIGN KEY (server_id) REFERENCES servers(id)
);

-- Таблица устройств (диски, сетевые интерфейсы и др.)
CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id INTEGER NOT NULL,
    name TEXT NOT NULL,          -- nvme0n1, eth0, etc.
    type TEXT NOT NULL,          -- 'disk', 'nic', 'gpu', etc.
    serial TEXT,
    model TEXT,
    FOREIGN KEY (server_id) REFERENCES servers(id)
);

-- Таблица тестовых утилит (fio, iperf, qperf, ...)
CREATE TABLE IF NOT EXISTS test_tools (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    version TEXT,       -- версия утилиты
    description TEXT
);

-- Таблица определения тестов с параметрами
CREATE TABLE IF NOT EXISTS test_definitions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    parameters TEXT,  -- JSON в виде строки
    FOREIGN KEY (tool_id) REFERENCES test_tools(id)
);

-- Таблица конкретных запусков тестов
CREATE TABLE IF NOT EXISTS test_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL,
    device_id INTEGER NOT NULL,
    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    duration_ms INTEGER,
    notes TEXT,
    FOREIGN KEY (test_id) REFERENCES test_definitions(id),
    FOREIGN KEY (device_id) REFERENCES devices(id)
);

-- Таблица метрик результата теста
CREATE TABLE IF NOT EXISTS test_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_run_id INTEGER NOT NULL,
    metrics TEXT NOT NULL,  -- JSON-строка с метриками
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (test_run_id) REFERENCES test_runs(id)
);

CREATE TABLE IF NOT EXISTS test_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_number TEXT NOT NULL,
    flavor TEXT,
    server_count INTEGER,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS server_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT,
    instance_id TEXT NOT NULL,
    ip_address TEXT,
    cpu_model TEXT,
    ram TEXT,
    disk_info TEXT,
    disk_count INTEGER,
    ping_result TEXT,
    speed_result TEXT,
    console_info TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (task_id) REFERENCES test_tasks(id) ON DELETE CASCADE
);