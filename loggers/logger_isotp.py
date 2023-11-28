import can
import osy_tp
from loggers import logger_utils
from loggers.logger_utils import CAN_INTERFACE
from loggers.logger_app import logger
from addresses import UDS_REQUEST_CAN_ID, UDS_RESPONSE_CAN_ID


LOG_TYPE = "isotp"


def start(dummy, stop_thread):
    uds_stack_req = create_stack(rxid=UDS_REQUEST_CAN_ID, txid=UDS_RESPONSE_CAN_ID)
    uds_stack_res = create_stack(rxid=UDS_RESPONSE_CAN_ID, txid=UDS_REQUEST_CAN_ID)

    file_path = logger_utils.create_file_path(LOG_TYPE)
    while not stop_thread():
        uds_stack_req.process()
        uds_stack_res.process()

        uds_request = uds_stack_req.recv()
        uds_response = uds_stack_res.recv()

        file_path = logger_utils.create_new_file_path_if_size_exceeded(file_path, LOG_TYPE)
        if uds_request is not None:
            logger_utils.write_to_file(file_path, None, UDS_REQUEST_CAN_ID, uds_request)
        if uds_response is not None:
            logger_utils.write_to_file(file_path, None, UDS_RESPONSE_CAN_ID, uds_response)
    uds_stack_req.bus.shutdown()
    uds_stack_res.bus.shutdown()


def create_stack(rxid, txid):
    try:
        bus = can.Bus(channel=CAN_INTERFACE, interface='socketcan')
    except Exception as exception:
        logger.error("Could not access can interface \"" + CAN_INTERFACE + "\". Exception type: " + type(exception).__name__ + ".")
    
    #configure isotp to use bus:
    tp_parameters = { "listen_mode" : True }
    address = osy_tp.Address(addressing_mode= osy_tp.AddressingMode.Normal_29bits, rxid=rxid, txid=txid, params=tp_parameters)
    stack = osy_tp.CanStack(bus, address=address)

    return stack

