import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "ecu_config.json")

CONFIG = json.load(open(CONFIG_FILE, "r"))

def get_server_project_file():
    return CONFIG["server_project_file"].get("value")


def get_uds_request_can_id():
    id = 0x18DA007E | (int(CONFIG["server_node_id"].get("value"))<< 8)
    return id


def get_uds_response_can_id():
    id = 0x18DA7E00 | int(CONFIG["server_node_id"].get("value"))
    return id


def create_address(address):
    try:
        return int(address, 16)
    except ValueError as error:
        print(error)
        exit(1)


def get_can_interface():
    return CONFIG["can_interface"].get("value")



