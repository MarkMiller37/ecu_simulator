from PySide6.QtWidgets import  QWidget, QTableWidgetItem, QMessageBox
from PySide6.QtCore import *
from ui_form import Ui_Widget
import osy_server


class DpEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        # show all data pool elements on table widget
        # columns: DP, list, element, size, value(editable)
        self.ui.tableWidget.setColumnCount(5)
        self.ui.tableWidget.setHorizontalHeaderLabels(["data_pool", "list", "element", "size", "value"])
        self.ui.tableWidget.setRowCount(osy_server.TheOpenSydeServer.get_number_of_data_pool_elements())
        row = 0
        for data_pool_index, data_pool in enumerate(osy_server.TheOpenSydeServer.datapools):
            for dp_list_index, dp_list in enumerate(data_pool.lists):
                for element_index, element in enumerate(dp_list.elements):
                    item_data_pool = QTableWidgetItem(data_pool.name)
                    item_data_pool.setFlags(item_data_pool.flags() ^ Qt.ItemIsEditable)

                    item_list = QTableWidgetItem(dp_list.name)
                    item_list.setFlags(item_data_pool.flags() ^ Qt.ItemIsEditable)

                    item_element = QTableWidgetItem(element.name)
                    item_element.setFlags(item_data_pool.flags() ^ Qt.ItemIsEditable)

                    item_size = QTableWidgetItem(str(element.size))
                    item_size.setFlags(item_data_pool.flags() ^ Qt.ItemIsEditable)

                    value = element.get_value()
                    valuestring = ""
                    for byte in value:
                        valuestring += f'{byte:02x}' #get byte as f-string and format in hex
                    item_value = QTableWidgetItem(valuestring)
                    # place dp,list,element index with cell item
                    item_value.setData(Qt.UserRole, data_pool_index)
                    item_value.setData(Qt.UserRole + 1, dp_list_index)
                    item_value.setData(Qt.UserRole + 2, element_index)

                    self.ui.tableWidget.setItem(row, 0, item_data_pool)
                    self.ui.tableWidget.setItem(row, 1, item_list)
                    self.ui.tableWidget.setItem(row, 2, item_element)
                    self.ui.tableWidget.setItem(row, 3, item_size)
                    self.ui.tableWidget.setItem(row, 4, item_value)
                    row += 1

        self.ui.tableWidget.setColumnWidth(0, 100)
        self.ui.tableWidget.setColumnWidth(1, 100)
        self.ui.tableWidget.setColumnWidth(2, 300)
        self.ui.tableWidget.setColumnWidth(3, 50)
        self.ui.tableWidget.setColumnWidth(4, 100)

        self.ui.tableWidget.itemChanged.connect(self.on_table_item_changed)


    def on_table_item_changed(self, item):
        #value column ?
        if item.column() == 4:
            dp_index = item.data(Qt.UserRole)
            list_index = item.data(Qt.UserRole + 1)
            element_index = item.data(Qt.UserRole + 2)

            element = osy_server.TheOpenSydeServer.datapools[dp_index].lists[list_index].elements[element_index]

            value_string = item.text()
            if len(value_string) != element.size * 2:
                message_box = QMessageBox()
                message_box.setText("Length of string does not match size of element.")
                message_box.exec()
                # back to original value:
                original_value = element.get_value()
                valuestring = ""
                for byte in original_value:
                    valuestring += f'{byte:02x}' #get byte as f-string and format in hex
                item.setText(valuestring)
                return

            try:
                value_bytes = bytes.fromhex(value_string)
            except Exception:
                message_box = QMessageBox()
                message_box.setText("Value does not seem to be a valid hex value.")
                message_box.exec()
                # back to original value:
                original_value = element.get_value()
                valuestring = ""
                for byte in original_value:
                    valuestring += f'{byte:02x}' #get byte as f-string and format in hex
                item.setText(valuestring)
                return

            element.set_value(value_bytes)
            print("DP value changed in GUI. Element: " + str(dp_index) + "." + str(list_index) + "." +
                  str(element_index) + ".")
