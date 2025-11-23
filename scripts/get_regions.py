import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tabulate import tabulate
from src.api.cloud import get_regions


def get_regions_table():
    """
    Fetches region data from GCore API using the centralized API function and displays it in a table.
    """
    try:
        regions = get_regions()

        table_data = [["ID", "Name", "Keystone Name"]]
        for region in regions:
            table_data.append([region.id, region.display_name, region.keystone_name])

        print(tabulate(table_data, headers="firstrow", tablefmt="orgtbl"))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_regions_table()