import isotp
import can
import ecu_config
import time
from uds import services
from addresses import UDS_REQUEST_CAN_ID, UDS_RESPONSE_CAN_ID
from loggers.logger_app import logger

CAN_INTERFACE = ecu_config.get_can_interface()


def start():
    uds_stack_req = create_stack(rxid=UDS_REQUEST_CAN_ID, txid=UDS_RESPONSE_CAN_ID)

    response = bytes([4]) 
    uds_stack_req.send(response)

    while True:
        #while uds_stack_req.transmitting():
        uds_stack_req.process()
        #time.sleep(uds_stack_req.sleep_time())

        request = uds_stack_req.recv()
        if request is not None:
            log_request(request)
            if len(request) >= 1:
                response = services.process_service_request(request)
                if response is not None:
                    log_response(response)
                    uds_stack_req.send(response)

def my_error_handler(error):
   logger.error('IsoTp error happened : %s - %s' % (error.__class__.__name__, str(error)))

def create_stack(rxid, txid):
    try:
        bus = can.Bus(channel=CAN_INTERFACE, interface='socketcan')
    except Exception as exception:
        logger.error("Could not access can interface \"" + CAN_INTERFACE + "\". Exception type: " + type(exception).__name__ + ".")
    
    #configure isotp to use bus:
    addressing = isotp.Address(addressing_mode= isotp.AddressingMode.Normal_29bits, rxid=rxid, txid=txid)

    #BSmax must be 0 for openSYDE; otherwise the client will not be happy    
    tp_parameters = { "blocksize" : 0 }
    stack = isotp.CanStack(bus, address=addressing, error_handler = my_error_handler, params=tp_parameters)

    return stack


def log_request(request):
    logger.info("Receiving on UDS address " + hex(UDS_REQUEST_CAN_ID) + " from " + hex(UDS_RESPONSE_CAN_ID)
                + " Request: 0x" + request.hex())


def log_response(response):
    logger.info("Sending to " + hex(UDS_REQUEST_CAN_ID) + " Response: 0x" + response.hex())