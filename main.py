from ui.main_window import Ui_MainWindow
from models.contact import Contact, ContactList
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
import json
import sys
import PyQt5
import csv


class ErrorMessage(QMessageBox):
    def __init__(self, parent=None):
        super(ErrorMessage, self).__init__(parent)
        self.setWindowTitle("Incorrect file type")
        self.setText("Warning")
        self.setIcon(QMessageBox.Information)
        self.setStandardButtons(QMessageBox.Cancel)
        self.setDefaultButton(QMessageBox.Cancel)

    def set_text(self, message):
        self.setInformativeText(f"{message}")

    def show_window(self):
        self.exec_()


class FileWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "File Explorer"
        self._screen_center = self.screen_center()
        self.width = 640
        self.height = 480
        self.left = self._screen_center.x() - self.width // 2
        self.top = self._screen_center.y() - self.height // 2
        self.file = None
        self.initUI()

    def screen_center(self):
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        return centerPoint

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()
        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            if fileName[-4:] == ".csv":
                self.file = fileName
            else:
                self.file = None


    @property
    def file_name(self) -> str:
        return self.file


class StartupWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        """
        in cmd
        set TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        set TWILIO_AUTH_TOKEN=your_auth_token
        """

        self.json_info = {
        }
        self.create_json()

    def create_json(self):
        # Serializing json
        json_object = json.dumps(self.json_info, indent=4)

        # Writing to sample.json
        with open("./settings.json", "w") as outfile:
            outfile.write(json_object)


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.contact_list: ContactList = None
        self.csv_variables_names: list[str] = None
        self.setWindowTitle("Ryan Green: Texting Program v0.1")

        # read json file for file name, use in csv if found
        self.csv_file_location = None  # https://stackoverflow.com/questions/19078170/python-how-would-you-save-a-simple-settings-config-file

        # clicked buttons
        self.btn_csv_input.clicked.connect(self.load_csv_file)
        self.btn_variables.clicked.connect(self.add_variable)
        self.ent_text_field.textChanged.connect(self.text_change)
        self.tbl_csv_viewer.clicked.connect(self.text_change)
        self.btn_send_message.clicked.connect(self.send_messages)

    def throw_error_window(self, error_text: str, error=None):
        messagebox = ErrorMessage(self)

        if error:
            messagebox.setText(f"{error_text}\nError Message: {error}")
        else:
            messagebox.setText(f"{error_text}")
        messagebox.show_window()

    def sanitize_message(self, message):
        bad_text = ["{", "}"]
        for char in message:
            if char in bad_text:
                raise ValueError("Illegal characters in message")

    def clear_all(self):
        self.ent_preview.setText("")
        self.ent_text_field.setText("")

    def send_messages(self):
        try:
            for contact in self.contact_list:

                # catches sanitize_message error if 'bad_text' is true
                try:
                    message = self.replace_variables_with_text(self.ent_text_field.toPlainText(), contact.info)
                    self.sanitize_message(message)
                except ValueError as error:
                    self.throw_error_window(error)
                    return
                try:
                    contact.text_contact(message)
                except KeyError as error:
                    self.throw_error_window(error)
        except TypeError as error:
            self.throw_error_window("Please load a CSV file in before sending a message", error)

        self.clear_all()


    def replace_variables_with_text(self, message: str, contact_info: dict):
        for i, key in enumerate(self.tbl_csv_viewer.horizontal_labels):
            csv_var = self.csv_variables_names[i]
            contact_info_key = contact_info.get(key)
            message = message.replace(csv_var, contact_info_key)

        return message

    def text_change(self):
        EMPTY = ""
        current_text = self.ent_text_field.toPlainText()

        if current_text == EMPTY:
            self.ent_preview.setText(EMPTY)
            return

        # catches no selected row error
        try:
            selected_row = self.tbl_csv_viewer.selectedItems()[0].row()
        except IndexError:
            selected_row = 0

        # catches no csv error
        try:
            contact_info = self.contact_list[selected_row].info
            current_text = self.replace_variables_with_text(current_text, contact_info)
            self.ent_preview.setText(current_text)
        except TypeError as error:
            self.throw_error_window(f"Please load a CSV file in before sending a message", error)

    def add_variable(self, action):
        # catches variable clicked before csv loaded error
        try:
            variable_name = action.text()
            cursor_pos = self.ent_text_field.textCursor()
            cursor_pos.insertText(variable_name)
        except AttributeError as error:
            self.throw_error_window(f"Please load a CSV file in before sending a message", error)

    def create_variable_menu(self):
        menu = PyQt5.QtWidgets.QMenu()
        menu.triggered.connect(self.add_variable)
        for variable_type in self.csv_variables_names:
            menu.addAction(variable_type)
        self.btn_variables.setMenu(menu)

    def load_csv_file(self):
        file_window = FileWindow()
        if file_window.file_name is None:  # error
            self.throw_error_window("The file you are attempting to select is not a .csv, please select a .csv file")
            return

        self.csv_file_location = file_window.file_name
        self.tbl_csv_viewer.generate_table(self.generate_objects())
        self.lbl_item.setText(f"Contacts: {len(self.contact_list)}")
        self.csv_variables_names = [f";;{item}::".replace(";;", "{{").replace("::", "}}") for item in self.tbl_csv_viewer.horizontal_labels]
        self.create_variable_menu()
        self.tbl_csv_viewer.resizeColumnsToContents()
        # todo write to json file to load later

    def generate_objects(self) -> ContactList:
        with open(self.csv_file_location) as file:
            dict_reader = csv.DictReader(file)
            for contact_info in dict_reader:
                contact = Contact(contact_info)
            self.contact_list = contact.list()
        return self.contact_list

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('')
    app_icon = QIcon('../icons/main_header_image.png')
    app.setWindowIcon(app_icon)
    win = Main()
    win.show()
    sys.exit(app.exec())