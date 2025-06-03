import logging
import json
import os
from datetime import datetime
from time import sleep
from src.api.baremetal import send_baremetal_create_request, get_instance_ip_address, get_baremetal_overview
from src.db.database import Database
from src.task_manager.task_manager import wait_for_task_sync
from src.infrastructure.server_checks import (
    check_config_over_ssh,
    check_console,
    check_ping_google,
    check_speed_test, count_physical_disk
)
from src.config.settings import TMP_PATH, JIRA_TASK_ID

logger = logging.getLogger(__name__)

<<<<<<< HEAD
def create_one_server(server_id: int, db: Database = None) -> None:
=======

def check_server(server_id: int, instance_id="xxx", ip_address="xxx") -> None:
>>>>>>> 549c3b8 (refactor server tasks;)
    """
    Checks the server with the given ID and returns data for reporting.

<<<<<<< HEAD
    Returns:
        Dictionary with report data: server_id, status, created_at, error, details,
        cpu, ram, disk, console_ok, ping, speed.
        :param server_id: Unique identifier for the server.
        :param db: Reports database.
=======
    Args:
        :param server_id: Unique identifier for the server.
        :param instance_id: Unique identifier for the instance.
        :param ip_address: IP address of the server to check.
>>>>>>> 549c3b8 (refactor server tasks;)
    """
    result = {
        "server_id": str(server_id),
        "status": "failed",
        "created_at": datetime.now().isoformat(),
        "error": None,
        "details": None,
        "cpu": None,
        "ram": None,
        "disk": None,
        "console_ok": None,
        "ping": None,
        "speed": None
    }

    if db is None:
        db = Database()

    try:
<<<<<<< HEAD
        # Create server
        task_ids = send_baremetal_create_request(server_id)
        task = wait_for_task_sync(task_ids.tasks[0], sleep_sec=10)
        instance_id = task.created_resources.instances[0]
        hostname = get_baremetal_overview(instance_id).name
        ip_address = get_instance_ip_address(instance_id)

        # Wait for server to boot
        sleep_sec = 150
        logger.info(f"Sleeping {sleep_sec} seconds to let instance {instance_id} boot")
        sleep(sleep_sec)

=======
>>>>>>> 549c3b8 (refactor server tasks;)
        # Perform checks
        config = check_config_over_ssh(ip_address, instance_id)
        disk_count = count_physical_disk(ip_address, instance_id)
        console_ok = check_console(instance_id)
        ping_result = check_ping_google(ip_address, instance_id)
        speed_result = check_speed_test(ip_address, instance_id)

        # Combine results for JSON
        config.update({
            "console_ok": console_ok,
            "ping": ping_result,
            "speed": speed_result,
            "ip_address": ip_address,
            "instance_id": instance_id,
            "disk_count": disk_count
        })

        # Save to JSON
        os.makedirs(TMP_PATH, exist_ok=True)
        json_file = os.path.join(TMP_PATH, f"{server_id}_config_{instance_id}_{ip_address}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        logger.info(f"Saved config to {json_file}")

        # Update result for CSV
        result.update({
            "status": "success",
            "details": f"Server {instance_id} created, IP: {ip_address}",
            "instance_id": instance_id,
            "ip_address": ip_address,
            "cpu": config.get("cpu"),
            "ram": config.get("ram"),
            "disk": config.get("disk"),
            "console_ok": str(config.get("console_ok")),
            "ping": config.get("ping"),
            "speed": config.get("speed"),
            "disk_count": config.get("disk_count")
        })

        #Save to DB
        db.save_baremetal_data(hostname, instance_id)
        db.save_test_report_data(task_id=JIRA_TASK_ID, **result)

    except Exception as e:
        logger.error(f"Error creating server {server_id}: {e}", exc_info=True)
        result["error"] = str(e)
        result["details"] = "Failed to create server"

        # Save error JSON
        error_config = {
            "cpu": "error",
            "ram": "error",
            "disk": "error",
            "ip_address": "error",
            "instance_id": "error",
            "console_ok": "error",
            "ping": "error",
            "speed": "error",
            "disk_count": "error"
        }
        os.makedirs(TMP_PATH, exist_ok=True)
        json_file = os.path.join(TMP_PATH, f"{server_id}_config_{instance_id}_{ip_address}.json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(error_config, f, indent=2)
        logger.info(f"Saved error config to {json_file}")

    logger.info(f"Check completed for server {server_id}: {result}")


def create_one_server(server_id: int) -> None:
    """
    Creates one server and checks its configuration.

    Args:
        :param server_id: Unique identifier for the server.
    """
    task_ids = send_baremetal_create_request(server_id)
    task = wait_for_task_sync(task_ids.tasks[0], sleep_sec=10)
    instance_id = task.created_resources.instances[0]
    ip_address = get_instance_ip_address(instance_id)

    # Wait for server to boot
    sleep_sec = 150
    logger.info(f"Sleeping {sleep_sec} seconds to let instance {instance_id} boot")
    sleep(sleep_sec)

    logger.info(f"Checking server {server_id} with instance ID {instance_id} and IP {ip_address}")
    check_server(server_id, instance_id=instance_id, ip_address=ip_address)
