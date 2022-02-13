from ui.main_window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from models.windows import ErrorWindow, StartupWindow, FileWindow, SuccessWindow
from models.objects import ContactList, UserSettings
import os.path, time, PyQt5, sys
from twilio.rest import Client


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.contact_list: ContactList = None       # gets loaded in from load_csv_file
        self.setWindowTitle("MassTextMessenger v0.1")
        self.lbl_last_mod.setHidden(False)

        # is_setup_needed loads proper variables for below
        self.user_settings = UserSettings()
        self.client: Client = None
        self.twilio_balance: float = None
        self.csv_variables_names: list[str] = None
        self.is_setup_needed()

        # text changed
        self.ent_text_field.textChanged.connect(self.text_change)

        # clicked buttons
        self.btn_csv_input.clicked.connect(self.load_csv_from_file_window)
        self.btn_variables.clicked.connect(self.add_variable)
        self.tbl_csv_viewer.clicked.connect(self.text_change)
        self.btn_send_message.clicked.connect(self.send_messages)
        self.btn_refresh.clicked.connect(self.load_csv_file)

    def setup_twilio_client(self):
        self.client = Client(
            self.user_settings.get_twilio_account_sid(),
            self.user_settings.get_twilio_auth_token()
        )

    def is_setup_needed(self):
        # loads setup window if environment variables are not set
        if self.user_settings.get_twilio_account_sid() is None:
            setup_window = StartupWindow(self)
            setup_window.show()
            return True
        else:
            self.setup_twilio_client()
            # checks if csv is in settings.json, loads csv if true
            if self.user_settings['csvLocation']:
                self.load_csv_file()
            self.refresh_twilio_balance()
            return False

    def refresh_twilio_balance(self):
        self.twilio_balance = self.client.api.v2010.account.balance.fetch().balance
        self.setWindowTitle(f"MassTextMessenger v0.1 | Balance: {self.twilio_balance}")

    def twilio_available_phone_numbers(self):
        return self.client.api.v2010.incoming_phone_numbers.list()

    def update_last_modified_date(self):
        self.lbl_last_mod.setHidden(False)
        self.lbl_last_mod.setText(f"Last Modified Date: {self.user_settings['csvLastModDate']}")

    def show_success_window(self, error_text: str, error=None):
        messagebox = SuccessWindow(self)

        if error:
            messagebox.setText(f"{error_text}\nSuccess Message: {error}")
        else:
            messagebox.setText(f"{error_text}")
        messagebox.show_window()

    def show_error_window(self, error_text: str, error=None):
        messagebox = ErrorWindow(self)

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
        count_success = 0
        count_failure = 0
        EMPTY = ""
        success = None

        # checks if message field is empty
        if self.ent_text_field.toPlainText() == EMPTY:
            self.show_error_window("Text message is empty")
            return

        # checks if user selected a phone number
        if self.user_settings.get_twilio_phone_number() is None:
            self.show_error_window("Select a phone number before sending the message")
            return

        try:
            for contact in self.contact_list:
                # catches sanitize_message error if 'bad_text' is true
                try:
                    message = self.replace_variables_with_text(self.ent_text_field.toPlainText(), contact.info)
                    self.sanitize_message(message)
                except ValueError as error:
                    self.show_error_window(error)
                    return
                try:
                    success = contact.text_contact(message)
                    if success is True:
                        count_success += 1
                    else:
                        count_failure += 1

                except KeyError as error:
                    self.show_error_window(error)
        except TypeError as error:
            self.show_error_window("Please load a CSV file in before sending a message", error)

        self.clear_all_fields()
        self.refresh_twilio_balance()
        self.show_success_window(f"{count_success} contacts texted successfully\n"
                                 f"{count_failure} contacts failed to send due to invalid phone number")

    def replace_variables_with_text(self, message: str, contact_info: dict):
        EMPTY = ""
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
            self.show_error_window(f"Please load a CSV file in before sending a message", error)

    def check_csv_data_is_not_empty(self, col_name: str):
        EMPTY = ""
        OFFSET = 1  # offsets 0th index for CSV rows
        col_name = col_name.replace("{{", "").replace("}}", "")

        cells_missing_data = []
        # adds missing data cells to list to display count
        for i, contact in enumerate(self.contact_list):
            if contact.info[col_name] == EMPTY:
                cells_missing_data.append(i + OFFSET)

            # ensures phone error pops up before missing data in cells error
            if contact.info['phone'] == EMPTY:
                raise ValueError(f"Phone column empty in row {i + OFFSET}")

        if cells_missing_data:
            raise ValueError(f"Col: {col_name} missing data in cells:\n{[str(int) for int in cells_missing_data]}")


    def add_variable(self, action):
        variable_name = action.text()

        try:
            self.check_csv_data_is_not_empty(variable_name)
        except ValueError as error:
            self.show_error_window(error)
            return

        # catches variable clicked before csv loaded error
        try:
            cursor_pos = self.ent_text_field.textCursor()
            cursor_pos.insertText(variable_name)
        except AttributeError as error:
            self.show_error_window(f"Please load a CSV file in before sending a message", error)

    def create_variable_menu(self):
        self.csv_variables_names = [f";;{item}::".replace(";;", "{{").replace("::", "}}") for item in self.tbl_csv_viewer.horizontal_labels]
        menu = PyQt5.QtWidgets.QMenu()
        menu.triggered.connect(self.add_variable)
        for variable_type in self.csv_variables_names:
            menu.addAction(variable_type)
        self.btn_variables.setMenu(menu)

    def select_phone_number_from_menu(self, action: PyQt5.QtWidgets.QAction):
        # catches variable clicked before csv loaded error
        try:
            phone_number_selected = action.text()[0:12]  #0:12 is string slicing the phone number
            self.user_settings.set_twilio_phone_number(phone_number_selected)
            self.lbl_selected_phone_number.setText(phone_number_selected)

            for item in self.client.messages.list(limit=100, to=self.user_settings.get_twilio_phone_number()):
                print(item.from_, item.to, item.body)

        except AttributeError as error:
            self.show_error_window(f"Please load a CSV file in before sending a message", error)

    def create_phone_number_menu(self):
        menu = PyQt5.QtWidgets.QMenu()
        menu.triggered.connect(self.select_phone_number_from_menu)
        for phone_number in self.twilio_available_phone_numbers():
            menu.addAction(f"{phone_number.phone_number} ({phone_number.friendly_name})")
        self.btn_phone_numbers.setMenu(menu)

    def load_csv_from_file_window(self):
        file_window = FileWindow()
        if file_window.file_name is None:  # error
            file_window.close()
            self.show_error_window("The file you are attempting to select is not a .csv, please select a .csv file")
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
        self.setup_twilio_client()
        self.lbl_last_mod.setHidden(False)
        self.clear_memory()
        try:
            self.contact_list = self.tbl_csv_viewer.generate_table(self.user_settings['csvLocation'])
        except (ValueError, UnboundLocalError) as error:
            self.show_error_window("could not load CSV", error)
            return
        self.lbl_item.setText(f"Contacts: {len(self.contact_list)}")
        self.create_variable_menu()
        self.create_phone_number_menu()
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