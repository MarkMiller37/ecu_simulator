import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "ecu_config.json")

CONFIG = json.load(open(CONFIG_FILE, "r"))


def get_uds_ecu_can_id():
    return create_address(CONFIG["uds_ecu_can_id"].get("value"))


def get_uds_client_can_id():
    return create_address(CONFIG["uds_client_can_id"].get("value"))


def create_address(address):
    try:
        return int(address, 16)
    except ValueError as error:
        print(error)
        exit(1)


def get_can_interface():
    return CONFIG["can_interface"].get("value")



