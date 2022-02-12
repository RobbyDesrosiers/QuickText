from ui.main_window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from models.windows import ErrorMessage, StartupWindow, FileWindow
from models.objects import ContactList, UserSettings
import os.path, time, PyQt5, sys


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.contact_list: ContactList = None
        self.setWindowTitle("MassTextMessenger v0.1")
        self.user_settings = UserSettings()
        self.is_setup_needed()

        # variables
        self.csv_variables_names: list[str] = None

        if self.user_settings['csvLocation']:
            self.load_csv_file()
        else:
            self.lbl_last_mod.setHidden(True)

        # clicked buttons
        self.btn_csv_input.clicked.connect(self.load_csv_from_file_window)
        self.btn_variables.clicked.connect(self.add_variable)
        self.ent_text_field.textChanged.connect(self.text_change)
        self.tbl_csv_viewer.clicked.connect(self.text_change)
        self.btn_send_message.clicked.connect(self.send_messages)

    def is_setup_needed(self):
        print(self.user_settings.get_twilio_account_sid())
        if self.user_settings.get_twilio_account_sid() is None:
            setup_window = StartupWindow(self)
            setup_window.show()

    def update_last_modified_date(self):
        self.lbl_last_mod.setHidden(False)
        self.lbl_last_mod.setText(self.user_settings['csvLastModDate'])

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

    def clear_all_fields(self):
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

        self.clear_all_fields()


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

    def load_csv_from_file_window(self):
        file_window = FileWindow()
        if file_window.file_name is None:  # error
            self.throw_error_window("The file you are attempting to select is not a .csv, please select a .csv file")
            return

        self.user_settings['csvLocation'] = file_window.file_name
        self.user_settings['csvLastModDate'] = time.ctime(os.path.getmtime(self.user_settings['csvLocation']))
        self.user_settings.save()
        self.load_csv_file()

    def clear_memory(self):
        try:
            self.tbl_csv_viewer.clear()
            self.contact_list.clear()
        except AttributeError as error:
            pass

    def load_csv_file(self):
        self.clear_memory()
        self.contact_list = self.tbl_csv_viewer.generate_table(self.user_settings['csvLocation'])
        self.lbl_item.setText(f"Contacts: {len(self.contact_list)}")
        self.csv_variables_names = [f";;{item}::".replace(";;", "{{").replace("::", "}}") for item in self.tbl_csv_viewer.horizontal_labels]
        self.create_variable_menu()
        self.tbl_csv_viewer.resizeColumnsToContents()
        self.update_last_modified_date()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setStyle('')
    # app_icon = QIcon('../icons/main_header_image.png')
    # app.setWindowIcon(app_icon)
    win = Main()
    win.show()
    sys.exit(app.exec())