import logging

import requests

from src.config.settings import SSH_KEY_PATH, PROJECT_ID, REGION_ID,PROD_API_KEY
import paramiko
from time import sleep

logger = logging.getLogger(__name__)


def create_ssh_client(ip_address, instance_id):
    """
    Creates and configures an SSH client to connect to the instance.

    Args:
        ip_address: IP address of the instance to connect to
        instance_id: Instance ID

    Returns:
        paramiko.SSHClient: The configured SSH client

    Raises:
        TimeoutError: If failed to connect after several attempts
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key = paramiko.RSAKey.from_private_key_file(SSH_KEY_PATH)

    return connect_ssh(ssh_client, ip_address, instance_id, private_key)


def connect_ssh(ssh_client, ip_address, instance_id, private_key, max_attempts=20, retry_interval=6):
    """
    Tries to establish an SSH connection to the specified instance with repeated attempts.

    Args:
        ssh_client: SSH client to connect to
        ip_address: IP address of the instance to connect to
        instance_id: Instance ID
        private_key: Key for SSH authentication
        max_attempts: Maximum number of connection attempts
        retry_interval: Interval between attempts in seconds

    Returns:
        paramiko.SSHClient: Connected SSH client

    Raises:
        TimeoutError: If failed to connect after max_attempts attempts
    """
    for attempt in range(1, max_attempts + 1):
        try:
            ssh_client.connect(ip_address, username="ubuntu", pkey=private_key)
            return ssh_client
        except Exception as e:
            logger.error(
                f"Failed to connect to {ip_address} of {instance_id} via SSH attempt {attempt} of {max_attempts}: {e}")
            if attempt < max_attempts:
                sleep(retry_interval)
                return None
            else:
                total_minutes = round(retry_interval * max_attempts / 60)
                raise TimeoutError(
                    f"Failed to connect to {ip_address} of {instance_id} after {total_minutes} minutes"
                )
    return None


def execute_ssh_command(ssh_client, command):
    """
    Executes the command over SSH and returns the result.

    Args:
        ssh_client: Connected SSH client
        command: command execution

    Returns:
        str: Result of command execution
    """
    _, stdout, _ = ssh_client.exec_command(command)
    return stdout.read().decode().strip()


def check_config_over_ssh(ip_address, instance_id):
    """
    Проверяет конфигурацию удаленного инстанса по SSH.

    Args:
        ip_address: IP address of the instance to be tested
        instance_id: Instance ID

    Returns:
        dict: Dictionary with configuration information (CPU, RAM, disk)

    Raises:
        TimeoutError: If unable to connect to the instance
    """
    logger.info(f"Checking config over SSH for {instance_id} at {ip_address}")

    ssh_client = create_ssh_client(ip_address, instance_id)

    try:
        cpu = execute_ssh_command(ssh_client, "cat /proc/cpuinfo | grep 'model name' | head -1")
        ram = execute_ssh_command(ssh_client, "free -h | grep Mem | awk '{print $2}'")
        disk = execute_ssh_command(ssh_client, "lsblk")

        results = {
            "cpu": cpu,
            "ram": ram,
            "disk": disk,
            "ip_address": ip_address,
            "instance_id": instance_id
        }

        logger.info(results)
        return results
    finally:
        ssh_client.close()


def check_ping_google(ip_address, instance_id):
    """
    Проверяет доступность google.com с удаленного инстанса.

    Args:
        ip_address: IP-адрес инстанса для проверки
        instance_id: Идентификатор инстанса

    Returns:
        str: Результат выполнения команды ping

    Raises:
        TimeoutError: Если не удалось подключиться к инстансу
    """
    logger.info(f"Checking ping to google.com {instance_id} at {ip_address}")

    ssh_client = create_ssh_client(ip_address, instance_id)

    try:
        ping_result = execute_ssh_command(ssh_client, "ping -c 3 google.com")
        logger.info(ping_result)
        return ping_result
    finally:
        ssh_client.close()

def check_console(instance_id) -> str:
    logger.info(f"Checking console for {instance_id}")
    url = f"https://api.gcore.com/cloud/v1/instances/{PROJECT_ID}/{REGION_ID}/{instance_id}/get_console"
    headers = {
        "Authorization": f"APIKey {PROD_API_KEY}"
    }
    response = requests.request("GET", url, headers=headers)
    s = f"{response.status_code} {response.text}"
    return s


def check_speed_test(ip_address, instance_id):
    """
    Checks Speedtest-cli speed result for instance

    Args:
        ip_address: IP address of the instance to be tested
        instance_id: Instance ID

    Returns:
        str: Speedtest result (Upload and Download speed)

    Raises:
        TimeoutError: If unable to connect to the instance
    """
    logger.info(f"Checking Speedtest for {instance_id}")
    ssh_client = create_ssh_client(ip_address, instance_id)
    command = 'curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python3 - | grep -E "Download|Upload"'
    try:
        result = execute_ssh_command(ssh_client, command=command)
        logger.debug(f"Speedtest result: {result}")
        return result
    finally:
        ssh_client.close()

def count_physical_disk(ip_address, instance_id) -> str:
    """
    Counts the number of physical disks on the server.

    Returns:
        str: Number of physical disks
    """
    logger.info(f"Checking ping to google.com {instance_id} at {ip_address}")

    ssh_client = create_ssh_client(ip_address, instance_id)
    command = 'lsblk -o TYPE,MODEL,SERIAL,VENDOR | grep -c "disk"'
    try:
        count = execute_ssh_command(ssh_client, command=command)
        logger.info(f"Counter of physical disks: {count}")
        return count
    finally:
        ssh_client.close()