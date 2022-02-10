from PyQt5.QtWidgets import QTextEdit, QPushButton, QTableWidget, QMessageBox
from models.objects import ContactList
import PyQt5

class CsvTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.column_count = 0
        self.contact_list = None
        self.setColumnCount(self.column_count)
        self._horizontal_labels = []
        self.setHorizontalHeaderLabels(self.horizontal_labels)

    @property
    def horizontal_labels(self):
        return self._horizontal_labels

    @horizontal_labels.setter
    def horizonal_labels(self, value):
        self._horizontal_labels = value

    def add_header(self, header_name: str):
        self.horizontal_labels.append(header_name)
        self.setColumnCount(self.columnCount() + 1)
        self.setHorizontalHeaderLabels(self.horizontal_labels)

    def calculate_col_widths(self):
        if self.column_count == 2:
            TABLE_WIDTHS = [60, 120]
        else:
            TABLE_WIDTHS = []
            for i in range(self.column_count):
                TABLE_WIDTHS.append(self.width() / self.column_count)

        return TABLE_WIDTHS

    def set_horizontal_labels(self):
        EMPTY = []

        # will load horizontal headers
        if self.horizontal_labels == EMPTY:
            for contact in self.contact_list:
                for column in contact.info:
                    self.horizontal_labels.append(column)
                self.column_count = len(self.horizontal_labels)
                break

        # if loaded, set the labels in the table (since we are most likely generating table)
        self.setHorizontalHeaderLabels(self.horizontal_labels)

    def generate_table(self, contacts: ContactList):
        self.contact_list = contacts
        self.set_horizontal_labels()
        ROW_HEIGHT = 10

        TABLE_WIDTHS = self.calculate_col_widths()


        contact_count = len(contacts)
        self.setRowCount(0)
        self.setRowCount(contact_count)
        self.setColumnCount(self.column_count)

        for row, contact in enumerate(contacts):
            self.setRowHeight(row, ROW_HEIGHT)
            for column in range(0, self.column_count):
                contact_info = contact.info
                self.setColumnWidth(column, TABLE_WIDTHS[column])
                self.setItem(row, column, PyQt5.QtWidgets.QTableWidgetItem(str(contact_info.get(self.horizontal_labels[column]))))

        self.set_horizontal_labels()


class VariableButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)


class Textbox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)