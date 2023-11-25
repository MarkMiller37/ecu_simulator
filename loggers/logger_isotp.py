import isotp
from loggers import logger_utils
from loggers.logger_utils import CAN_INTERFACE
from loggers.logger_app import logger
from addresses import UDS_ECU_CAN_ID, UDS_CLIENT_CAN_ID


LOG_TYPE = "isotp"


def start():
    uds_socket_req = create_socket(rxid=UDS_ECU_CAN_ID, txid=UDS_CLIENT_CAN_ID)
    uds_socket_res = create_socket(rxid=UDS_CLIENT_CAN_ID, txid=UDS_ECU_CAN_ID)

    file_path = logger_utils.create_file_path(LOG_TYPE)
    while True:
        uds_request = uds_socket_req.recv()
        uds_response = uds_socket_res.recv()

        file_path = logger_utils.create_new_file_path_if_size_exceeded(file_path, LOG_TYPE)
        if uds_request is not None:
            logger_utils.write_to_file(file_path, None, UDS_ECU_CAN_ID, uds_request)
        if uds_response is not None:
            logger_utils.write_to_file(file_path, None, UDS_CLIENT_CAN_ID, uds_response)


def create_socket(rxid, txid):
    socket = isotp.socket()
    socket.set_opts(socket.flags.LISTEN_MODE)
    try:
       socket.bind(CAN_INTERFACE, isotp.Address(addressing_mode=isotp.AddressingMode.Normal_29bits, rxid=rxid, txid=txid))
    except:
       logger.error("Could not bind to \"" + CAN_INTERFACE + "\". Does the interface exist ?")
    return socket

