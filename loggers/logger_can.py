import can
from loggers import logger_utils
from addresses import UDS_REQUEST_CAN_ID, UDS_RESPONSE_CAN_ID

LOG_TYPE = "can"
BUS_TYPE = "socketcan"

CAN_MASK = 0x7FF


def start(dummy, stop_thread):
    bus = create_can_bus()
    file_path = logger_utils.create_file_path(LOG_TYPE)
    while not stop_thread():
        file_path = logger_utils.create_new_file_path_if_size_exceeded(file_path, LOG_TYPE)
        message = bus.recv(0.1)
        if message is not None:
           logger_utils.write_to_file(file_path, message.timestamp, message.arbitration_id, message.data)
    bus.shutdown()


def create_can_bus():
    return can.interface.Bus(channel=logger_utils.CAN_INTERFACE, bustype=BUS_TYPE, can_filters=get_filters())


def get_filters():
    filters = []
    filters.append({"can_id": UDS_REQUEST_CAN_ID, "can_mask": CAN_MASK, "extended": True})
    filters.append({"can_id": UDS_RESPONSE_CAN_ID, "can_mask": CAN_MASK, "extended": True})
    return filters

