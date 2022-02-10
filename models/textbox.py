from PyQt5.QtWidgets import QTextEdit

class Textbox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)