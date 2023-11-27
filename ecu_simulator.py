import sys
from threading import Thread
import ecu_config
import osy_server
from uds import listener as uds_listener
from loggers import logger_app, logger_can, logger_isotp


def main():
    logger_app.configure()
    logger_app.logger.info("Starting ECU-Simulator")

    project_path = ecu_config.get_server_project_file()

    try:
        osy_server.TheOpenSydeServer.LoadDefinitionFromXml(xml_path=project_path)
    except Exception:
        logger_app.logger.error("Could not load server configuration.")

    start_can_logger_thread()
    start_isotp_logger_thread()
    start_uds_listener_thread()


def start_can_logger_thread():
    Thread(target=logger_can.start).start()


def start_isotp_logger_thread():
    Thread(target=logger_isotp.start).start()


def start_uds_listener_thread():
    Thread(target=uds_listener.start).start()


if __name__ == '__main__':
    sys.exit(main())
