import csv
import json
import logging
import os
from typing import List
from src.config.settings import REPORT_FILE, TMP_PATH

logger = logging.getLogger(__name__)


class CSVReporter:
    def __init__(self, report_file: str = REPORT_FILE, json_dir: str = TMP_PATH):
        self.report_file = report_file
        self.json_dir = json_dir
        os.makedirs(os.path.dirname(self.report_file), exist_ok=True)
        logger.debug(f"Report file path: {os.path.abspath(self.report_file)}")
        logger.debug(f"JSON directory: {os.path.abspath(self.json_dir)}")

    def write_report(self) -> None:
        logger.info("Creating CSV report")

        # Find and sort JSON files
        json_filenames = sorted(
            [f for f in os.listdir(self.json_dir) if f.lower().endswith(".json")],
            key=lambda x: int(x.split("_")[0])
        )
        logger.info(f"Found {len(json_filenames)} JSON files")

        # Initialize data list
        data: List[List[str]] = []

        # Process each JSON file
        for filename in json_filenames:
            try:
                with open(os.path.join(self.json_dir, filename), "r", encoding="utf-8") as f:
                    json_data = json.load(f)

                # Extract server_id from filename
                server_id = filename.split("_")[0]

                # Extract data from JSON
                cpu = json_data.get("cpu", "error")
                # Handle original format if cpu contains a prefix like "cpu: 4 cores"
                if ":" in cpu:
                    cpu = cpu.split(":")[-1].strip()
                ram = json_data.get("ram", "error")
                disk = json_data.get("disk", "error")
                ip_address = json_data.get("ip_address", "error")
                instance_id = json_data.get("instance_id", "error")
                console_ok = json_data.get("console_ok", "error")
                ping = json_data.get("ping", "error")
                speed = json_data.get("speed", "error")
                disk_count = json_data.get("disk_count", "error")

                data.append([
                    server_id, cpu, ram, disk, disk_count, ip_address,
                    instance_id, str(console_ok), ping, speed
                ])
            except Exception as e:
                logger.error(f"Error processing JSON file {filename}: {e}")
                continue

        logger.info(f"Writing CSV report to {self.report_file}")
        with open(self.report_file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Server ID", "CPU", "RAM", "Disk", "Disk Count", "IP Address",
                             "Instance ID", "Console OK", "Ping", "Speed"])
            writer.writerows(data)