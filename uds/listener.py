import isotp
import ecu_config
from uds import services
from addresses import UDS_ECU_CAN_ID, UDS_CLIENT_CAN_ID
from loggers.logger_app import logger

CAN_INTERFACE = ecu_config.get_can_interface()


def start():
    isotp_socket = create_isotp_socket(UDS_ECU_CAN_ID, UDS_CLIENT_CAN_ID)
    while True:
        request = isotp_socket.recv()
        if request is not None:
            log_request(request)
            if len(request) >= 1:
                response = services.process_service_request(request)
                if response is not None:
                    log_response(response)
                    isotp_socket.send(response)


def create_isotp_socket(receiver_address, target_address):
    socket = isotp.socket()
    try:
       socket.bind(CAN_INTERFACE, isotp.Address(addressing_mode=isotp.AddressingMode.Normal_29bits, rxid=receiver_address, txid=target_address))
    except:
       logger.error("Could not bind to \"" + CAN_INTERFACE + "\". Does the interface exist ?")
    return socket


def log_request(request):
    logger.info("Receiving on UDS address " + hex(UDS_ECU_CAN_ID) + " from " + hex(UDS_CLIENT_CAN_ID)
                + " Request: 0x" + request.hex())


def log_response(response):
    logger.info("Sending to " + hex(UDS_ECU_CAN_ID) + " Response: 0x" + response.hex())