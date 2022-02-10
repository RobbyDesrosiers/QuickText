from PyQt5.QtWidgets import QMessageBox

class Popup:
    def error(self, error_msg):
        msg = QMessageBox()
        msg.setWindowTitle("Insufficient Information")
        msg.setText("Warning: Error")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setInformativeText(f"{error_msg}")
        msg.show()


    def success(self, success_msg):
        msg = QMessageBox()
        msg.setWindowTitle("Order Edit Submitted")
        msg.setText("ACCEPTED")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setInformativeText(f"{success_msg}")
        msg.show()


    def warning(self, success_msg):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText("Warning")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        msg.setInformativeText(f"{success_msg}")
        msg.show()