import ecu_config as ecu_config
import time
import os
import xml.etree.ElementTree as ElementTree

from loggers.logger_app import logger

class DataPool:
    name = ""
    version = [3]
    elements = []

    def __init__(self):
        self.name = ""

    def LoadDefinitionFromXml(self, xml_path):
        tree = ElementTree.parse(xml_path)
        if tree == None:
            logger.error("DataPool: Could not load \"" + xml_path + "\": Failed to parse file.")
            raise Exception()

        root = tree.getroot()

        element = root.find("file-version")
        if element == None:
            logger.error("DataPool: Could not load \"" + xml_path + "\": \"file-version\" node not found.")
            raise Exception()
        if element.text != "1":
            logger.error("DataPool: Could not load \"" + xml_path + "\": unsupported file version.")
            raise Exception()
        
        data_pool = root.find("data-pool")
        self.name = data_pool.find("name").text
        version = data_pool.find("version")
        self.version = bytes([int(version.attrib.get("major")), int(version.attrib.get("minor")), int(version.attrib.get("release"))])

        lists = data_pool.find("lists")
        list_index = 0
        for list in lists:
            #should only contain "list" nodes
            #for our purpose we only create a flat dictionary with basic information we need to provide DP values
            elements = list.find("data-elements")
            element_index = 0
            for element in elements:
               #should only contain "data-element" nodes
               type = element.find("type").attrib.get("base-type")
               is_array = element.find("type").attrib.get("is-array")
               if is_array != "false":
                   #todo: add support for arrays
                   logger.error("DataPool: Could not load \"" + xml_path + "\": Contains element which is defined as an array.")
                   raise Exception()
               if type == "uint8" or type == "sint8":
                   size = 1
               elif type == "uint16" or type == "sint16":
                   size = 2
               elif type == "uint32" or type == "sint32" or type == "float32":
                   size = 4
               elif type == "uint64" or type == "sint64" or type == "float64":
                   size = 8
               else:
                   logger.error("DataPool: Could not load \"" + xml_path + "\": Contains element with unknown type " + type + ".")
                   return None
               new_element = { "list": list_index, "element": element_index, "size": size}
               self.elements.append(new_element)
               element_index += 1
            list_index += 1
        

class OpenSydeServer:
    #configuration of this server
    name = ""
    datapools = []

    #current state of ECU simulation
    current_session = 0x01 #default session
    current_data_rates = [100,500,1000]
    #list of currently configured event based transmissions
    #elements: "data_pool", "list", "element", "rail", "last_send_time"
    current_event_based_transmissions = []
    current_last_event_based_send_times = [0,0,0]

    def __init__(self):
        self.name = ""

    #Load server definition from XML file.
    #A "node_core.xml" file which is part of an openSYDE project should be passed here.
    def LoadDefinitionFromXml(self, xml_path):
        tree = ElementTree.parse(xml_path)
        if tree == None:
            logger.error("OpenSydeServer: Could not load \"" + xml_path + "\": Failed to parse file.")
            raise Exception()

        root = tree.getroot()

        element = root.find("file-version")
        if element == None:
            logger.error("OpenSydeServer: Could not load \"" + xml_path + "\": \"file-version\" node not found.")
            raise Exception()
        if element.text != "1":
            logger.error("OpenSydeServer: Could not load \"" + xml_path + "\": unsupported file version.")
            raise Exception()

        #from here on we expect we really have a valid file; limited error handling done ...
        node = root.find("node")
        element = node.find("properties").find("name")
        self.name = element.text

        data_pools = node.find("data-pools")
        #should only contain "data-pool" nodes
        for data_pool in data_pools:
            new_data_pool = DataPool()
            data_pool_file_path = os.path.dirname(xml_path) + "/" + data_pool.text
            try:
               new_data_pool.LoadDefinitionFromXml(xml_path = data_pool_file_path)
            except:
               raise
            self.datapools.append(new_data_pool)

TheOpenSydeServer = OpenSydeServer()
