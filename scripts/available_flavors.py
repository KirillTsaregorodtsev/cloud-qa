from gcore.types.cloud import BaremetalFlavorList
from tabulate import tabulate

from src.api.baremetal import get_baremetal_flavors
from src.config.settings import REGION_ID

region = REGION_ID

def check_flavor_if_exist(flavor_list: BaremetalFlavorList, flavor: str) -> bool:
    for fl in flavor_list.results:
        if fl.flavor_id == flavor:
            print(f"Flavor exists: {flavor} = {fl.capacity}")
            return True
    print(f"Flavor does not exists: {flavor} in region: {region}")
    return False

def show_flavors_table(flavor_list: BaremetalFlavorList) -> None:
    table_data = [(flavor.flavor_id, flavor.capacity) for flavor in flavor_list.results]
    headers = ["Flavor ID", "Capacity"]
    print(tabulate(table_data, headers=headers, tablefmt="orgtbl"))

if __name__ == '__main__':
    FLAVOR = "bm1-hf-medium"
    flavors = get_baremetal_flavors()

    check_flavor_if_exist(flavors, FLAVOR)
    show_flavors_table(flavors)