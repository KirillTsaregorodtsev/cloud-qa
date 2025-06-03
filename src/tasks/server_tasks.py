import logging
import json
import os
from datetime import datetime
from time import sleep
from src.api.baremetal import send_baremetal_create_request, get_instance_ip_address
from src.task_manager.task_manager import wait_for_task_sync
from src.infrastructure.server_checks import (
    check_config_over_ssh,
    check_console,
    check_ping_google,
    check_speed_test, count_physical_disk
)
from src.config.settings import TMP_PATH

logger = logging.getLogger(__name__)

def create_one_server(server_id: int) -> None:
    """
    Creates a server with the given ID and returns data for reporting.

    Args:
        server_id: Unique identifier for the server.

    Returns:
        Dictionary with report data: server_id, status, created_at, error, details,
        cpu, ram, disk, console_ok, ping, speed.
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
    instance_id = "xxx"
    ip_address = "xxx"

    try:
        # Create server
        task_ids = send_baremetal_create_request(server_id)
        task = wait_for_task_sync(task_ids.tasks[0], sleep_sec=10)
        instance_id = task.created_resources.instances[0]
        ip_address = get_instance_ip_address(instance_id)

        # Wait for server to boot
        sleep_sec = 150
        logger.info(f"Sleeping {sleep_sec} seconds to let instance {instance_id} boot")
        sleep(sleep_sec)

        # Perform checks
        config = check_config_over_ssh(ip_address, instance_id)
        disk_count = count_physical_disk(ip_address, instance_id)
        console_ok = check_console(instance_id)
        ping_result = check_ping_google(ip_address, instance_id)
        speed_result = check_speed_test()

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
