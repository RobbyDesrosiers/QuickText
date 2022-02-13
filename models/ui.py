import csv

import phonenumbers
from PyQt5.QtWidgets import QTextEdit, QPushButton, QTableWidget, QMessageBox
from models.objects import ContactList, Contact
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
    def horizonal_labels(self, value: str):
        self._horizontal_labels = value.lower()

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

    def generate_table(self, csv_file_location):
        EMPTY = ""
        contacts = self.generate_objects(csv_file_location)
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
                self.setColumnWidth(column, TABLE_WIDTHS[column])
                # if contact.info.get(self.horizontal_labels[column]) == EMPTY:
                #     raise ValueError("Cell in CSV is empty, ensure all cells have data")
                self.setItem(row, column, PyQt5.QtWidgets.QTableWidgetItem(str(contact.info.get(self.horizontal_labels[column]))))

        self.set_horizontal_labels()
        return contacts

    def generate_objects(self, csv_file_location) -> ContactList:
        OFFSET = 1  # used for col offset because 0th index

        with open(csv_file_location) as file:
            dict_reader: list[dict] = csv.DictReader(file)

            for i, contact_info in enumerate(dict_reader):

                # iterates over first contact once, to check for phone column
                if not contact_info.get('phone'):
                    raise ValueError("CSV needs 'phone' column, please insert a column named: phone")

                # bad idea... moving this to send_messages
                # if not phonenumbers.is_valid_number(phonenumbers.parse(f"+1{contact_info.get('phone')}")):
                #     raise ValueError(f"Phone number in column {i} is invalid")


                contact = Contact(contact_info)
            self.contact_list = contact.list()
        return self.contact_list


class VariableButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)


class Textbox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)