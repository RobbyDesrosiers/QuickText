import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QWidget, QFileDialog
import PyQt5

from models.objects import UserSettings
from ui.main_window import Ui_MainWindow
from ui.setup_window import Ui_SetupWindow
from ui.test_window import Ui_test_mode
import json


class ErrorWindow(QMessageBox):
    def __init__(self, parent=None):
        super(ErrorWindow, self).__init__(parent)
        self.setWindowTitle("Warning: Error")
        self.setText("Warning")
        self.setIcon(QMessageBox.Critical)
        self.setStandardButtons(QMessageBox.Close)
        self.setDefaultButton(QMessageBox.Close)

    def set_text(self, message):
        self.setInformativeText(f"{message}")

    def show_window(self):
        self.exec_()

class SuccessWindow(QMessageBox):
    def __init__(self, parent=None):
        super(SuccessWindow, self).__init__(parent)
        self.setWindowTitle("Success")
        self.setText("Success")
        self.setIcon(QMessageBox.Information)
        self.setStandardButtons(QMessageBox.Close)
        self.setDefaultButton(QMessageBox.Close)

    def set_text(self, message):
        self.setInformativeText(f"{message}")

    def show_window(self):
        self.exec_()


class ConsoleWindow(QMainWindow, Ui_test_mode):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Message Console")

    def write_to_console(self, messages):
        for message in messages:
            self.console.append(f"{message}")

class StartupWindow(QMainWindow, Ui_SetupWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Twilio Information")
        self.user_settings = UserSettings()
        self.ent_account_sid.setEchoMode(PyQt5.QtWidgets.QLineEdit.Password)
        self.ent_auth_token.setEchoMode(PyQt5.QtWidgets.QLineEdit.Password)
        self.btn_submit.clicked.connect(self.submit)
        self.btn_cancel.clicked.connect(self.close)
        self.check_test_mode.stateChanged.connect(self.execute_test_mode)

    def execute_test_mode(self):
        self.user_settings.set_test_mode(True)
        self.close()

    def submit(self):
        try:
            self.user_settings.set_twilio_account_sid(self.ent_account_sid.text())
            self.user_settings.set_twilio_auth_token(self.ent_auth_token.text())
            self.close()
        except ValueError as error:
            self.throw_error_window("Cannot set account information", error)
            return

    def throw_error_window(self, error_text: str, error=None):
        messagebox = ErrorWindow(self)

        if error:
            messagebox.setText(f"{error_text}\nError Message: {error}")
        else:
            messagebox.setText(f"{error_text}")
        messagebox.show_window()

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
        # self.show()

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