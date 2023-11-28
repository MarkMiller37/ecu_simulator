import sys
import time
from threading import Thread
from PySide6.QtWidgets import QApplication
import ecu_config
import osy_server
from uds import listener as uds_listener
from loggers import logger_app, logger_can, logger_isotp

from dp_editor_gui import DpEditorWidget


def main():
    app = QApplication(sys.argv)

    stop_threads = False

    logger_app.configure()
    logger_app.logger.info("Starting ECU-Simulator")

    project_path = ecu_config.get_server_project_file()

    try:
        osy_server.TheOpenSydeServer.LoadDefinitionFromXml(xml_path=project_path)
    except Exception:
        logger_app.logger.error("Could not load server configuration.")

    #initialize and populate GUI:
    the_editor_widget = DpEditorWidget()
    the_editor_widget.show()

    dummy = 0 # first parameter of args needs to be integer
    can_logger_thread = Thread(target = logger_can.start, args=(dummy, lambda: stop_threads))
    iso_tp_logger_thread = Thread(target = logger_isotp.start, args=(dummy, lambda: stop_threads))
    uds_listener_thread = Thread(target = uds_listener.start, args=(dummy, lambda: stop_threads))

    can_logger_thread.start()
    iso_tp_logger_thread.start()
    uds_listener_thread.start()

    # show GUI; will block until widget is closed
    app.exec()

    print("Asking threads to shut down ...")
    stop_threads = True
    while can_logger_thread.is_alive() or iso_tp_logger_thread.is_alive() or uds_listener_thread.is_alive():
        time.sleep(0.1)

    print("Shutting down application ...")



def start_can_logger_thread():
    Thread(target=logger_can.start).start()


def start_isotp_logger_thread():
    Thread(target=logger_isotp.start).start()


def start_uds_listener_thread():
    Thread(target=uds_listener.start).start()


if __name__ == '__main__':
    sys.exit(main())
