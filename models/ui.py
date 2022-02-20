import csv

import phonenumbers
from PyQt5.QtWidgets import QTextEdit, QPushButton, QTableWidget, QMessageBox
from models.objects import ContactList, Contact, UserSettings
import PyQt5

class CsvTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_settings = UserSettings()
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
        self.set_horizontal_labels()
        ROW_HEIGHT = 10

        contact_count = len(contacts)
        self.setRowCount(0)
        self.setRowCount(contact_count)
        self.setColumnCount(self.column_count)

        for row, contact in enumerate(contacts):
            self.setRowHeight(row, ROW_HEIGHT)
            for column in range(0, self.column_count):
                self.setItem(row, column, PyQt5.QtWidgets.QTableWidgetItem(str(contact.info.get(self.horizontal_labels[column]))))
        self.set_horizontal_labels()

    def generate_objects(self, csv_file_location) -> ContactList:
        row_count = 0
        try:
            with open(csv_file_location) as file:
                dict_reader: list[dict] = csv.DictReader(file)

                for i, contact_info in enumerate(dict_reader):
                    row_count += 1
                    # iterates over first contact once, to check for phone column
                    if not contact_info.get('phone'):
                        raise ValueError("CSV needs 'phone' column, please insert a column named: phone")
                    contact = Contact(contact_info, test_mode=self.user_settings.get_test_mode())
        except FileNotFoundError:
            raise ValueError("Previously loaded CSV file not found")

        if row_count > 499:
            raise ValueError("CSV is over 500 rows long, please reduce to < 500")
        self.contact_list = contact.list()
        return self.contact_list

class VariableButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)


class Textbox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)