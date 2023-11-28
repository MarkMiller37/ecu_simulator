import os
import threading
import xml.etree.ElementTree as ElementTree

from loggers.logger_app import logger

class Element:
    def __init__(self):
        self.name = ""
        self.size = 0
        self.value = bytes(0)

        self.value_lock = threading.Lock()

    def set_value(self, value):
        self.value_lock.acquire()
        self.value = value
        self.value_lock.release()

    def get_value(self):
        self.value_lock.acquire()
        value = self.value
        self.value_lock.release()
        return value


class List:
    def __init__(self):
        self.name = ""
        self.elements = []


class DataPool:
    def __init__(self):
        self.name = ""
        self.version = [3]
        self.lists = []

    def load_definition_from_xml(self, xml_path):
        xml_tree = ElementTree.parse(xml_path)
        if xml_tree is None:
            logger.error("DataPool: Could not load \"%s\": Failed to parse file.", xml_path)
            raise SyntaxError()

        xml_root = xml_tree.getroot()

        xml_element = xml_root.find("file-version")
        if xml_element is None:
            logger.error("DataPool: Could not load \"%s\": \"file-version\" node not found.", xml_path)
            raise SyntaxError()
        if xml_element.text != "1":
            logger.error("DataPool: Could not load \"%s\":unsupported file version.", xml_path)
            raise SyntaxError()

        xml_data_pool = xml_root.find("data-pool")
        self.name = xml_data_pool.find("name").text
        xml_version = xml_data_pool.find("version")
        self.version = bytes([int(xml_version.attrib.get("major")), int(xml_version.attrib.get("minor")),
                              int(xml_version.attrib.get("release"))])

        xml_lists = xml_data_pool.find("lists")
        list_index = 0
        for xml_dp_list in xml_lists:
            #should only contain "list" nodes
            new_list = List()
            new_list.name = xml_dp_list.find("name").text

            xml_elements = xml_dp_list.find("data-elements")
            element_index = 0
            for xml_element in xml_elements:
                #should only contain "data-element" nodes
                new_element = Element()
                new_element.name = xml_element.find("name").text

                element_type = xml_element.find("type").attrib.get("base-type")
                is_array = xml_element.find("type").attrib.get("is-array")
                if is_array != "false":
                    #todo: add support for arrays
                    logger.error("DataPool: Could not load \"%s\": Contains element which is defined as an array.",
                                 xml_path)
                    raise SyntaxError()
                if element_type == "uint8" or element_type == "sint8":
                    size = 1
                elif element_type == "uint16" or element_type == "sint16":
                    size = 2
                elif element_type == "uint32" or element_type == "sint32" or element_type == "float32":
                    size = 4
                elif element_type == "uint64" or element_type == "sint64" or element_type == "float64":
                    size = 8
                else:
                    logger.error("DataPool: Could not load \"%s\": Contains element with unknown type %s.",
                                 xml_path, element_type)
                    return None
                new_element.size = size
                new_element.set_value(bytes([0] * size))
                new_list.elements.append(new_element)
                element_index += 1
            self.lists.append(new_list)
            list_index += 1


class OpenSydeServer:
    def __init__(self):
        #configuration of this server
        self.name = ""
        self.datapools = []

        #current state of ECU simulation
        self.current_session = 0x01 #default session
        self.current_data_rates = [100,500,1000]
        #list of currently configured event based transmissions
        #elements: "data_pool", "list", "element", "rail"
        self.current_event_based_transmissions = []
        self.current_last_event_based_send_times = [0,0,0]

    def get_number_of_data_pool_elements(self):
        number = 0
        for data_pool in self.datapools:
            for dp_list in data_pool.lists:
                number += len(dp_list.elements)
        return number

    #Load server definition from XML file.
    #A "node_core.xml" file which is part of an openSYDE project should be passed here.
    def load_definition_from_xml(self, xml_path):
        xml_tree = ElementTree.parse(xml_path)
        if xml_tree is None:
            logger.error("OpenSydeServer: Could not load \"%s\": Failed to parse file.", xml_path)
            raise SyntaxError()

        xml_root = xml_tree.getroot()

        xml_element = xml_root.find("file-version")
        if xml_element is None:
            logger.error("OpenSydeServer: Could not load \"%s\":\"file-version\" node not found.", xml_path)
            raise SyntaxError()
        if xml_element.text != "1":
            logger.error("OpenSydeServer: Could not load \"%s\": unsupported file version.", xml_path)
            raise SyntaxError()

        #from here on we expect we really have a valid file; limited error handling done ...
        xml_node = xml_root.find("node")
        xml_element = xml_node.find("properties").find("name")
        self.name = xml_element.text

        xml_data_pools = xml_node.find("data-pools")
        #should only contain "data-pool" nodes
        for xml_data_pool in xml_data_pools:
            new_data_pool = DataPool()
            data_pool_file_path = os.path.dirname(xml_path) + "/" + xml_data_pool.text
            try:
                new_data_pool.load_definition_from_xml(xml_path = data_pool_file_path)
            except SyntaxError:
                raise
            self.datapools.append(new_data_pool)

# Singleton of the server
TheOpenSydeServer = OpenSydeServer()
