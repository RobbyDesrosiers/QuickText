# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 500)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 500))
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 500))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.stacked_frame = QtWidgets.QStackedWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.stacked_frame.sizePolicy().hasHeightForWidth())
        self.stacked_frame.setSizePolicy(sizePolicy)
        self.stacked_frame.setObjectName("stacked_frame")
        self.quick_text_widget = QtWidgets.QWidget()
        self.quick_text_widget.setObjectName("quick_text_widget")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.quick_text_widget)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label = QtWidgets.QLabel(self.quick_text_widget)
        self.label.setMaximumSize(QtCore.QSize(400, 100))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(".\\ui\\quicksent_logo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lbl_last_mod = QtWidgets.QLabel(self.quick_text_widget)
        self.lbl_last_mod.setText("")
        self.lbl_last_mod.setObjectName("lbl_last_mod")
        self.gridLayout_3.addWidget(self.lbl_last_mod, 0, 0, 1, 2)
        self.tbl_csv_viewer = CsvTable(self.quick_text_widget)
        self.tbl_csv_viewer.setMaximumSize(QtCore.QSize(160000, 16777215))
        self.tbl_csv_viewer.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tbl_csv_viewer.setObjectName("tbl_csv_viewer")
        self.tbl_csv_viewer.setColumnCount(0)
        self.tbl_csv_viewer.setRowCount(0)
        self.gridLayout_3.addWidget(self.tbl_csv_viewer, 1, 0, 1, 3)
        self.btn_refresh = QtWidgets.QPushButton(self.quick_text_widget)
        self.btn_refresh.setMaximumSize(QtCore.QSize(71, 16777215))
        self.btn_refresh.setObjectName("btn_refresh")
        self.gridLayout_3.addWidget(self.btn_refresh, 2, 1, 1, 1)
        self.btn_csv_input = QtWidgets.QPushButton(self.quick_text_widget)
        self.btn_csv_input.setMaximumSize(QtCore.QSize(71, 16777215))
        self.btn_csv_input.setObjectName("btn_csv_input")
        self.gridLayout_3.addWidget(self.btn_csv_input, 2, 2, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 1, 3, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lbl_text = QtWidgets.QLabel(self.quick_text_widget)
        self.lbl_text.setObjectName("lbl_text")
        self.gridLayout_2.addWidget(self.lbl_text, 0, 0, 1, 1)
        self.ent_text_field = Textbox(self.quick_text_widget)
        self.ent_text_field.setMaximumSize(QtCore.QSize(800, 16777215))
        self.ent_text_field.setObjectName("ent_text_field")
        self.gridLayout_2.addWidget(self.ent_text_field, 1, 0, 1, 4)
        self.lbl_selected_phone_number = QtWidgets.QLabel(self.quick_text_widget)
        self.lbl_selected_phone_number.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lbl_selected_phone_number.setText("")
        self.lbl_selected_phone_number.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_selected_phone_number.setObjectName("lbl_selected_phone_number")
        self.gridLayout_2.addWidget(self.lbl_selected_phone_number, 2, 1, 1, 1)
        self.btn_phone_numbers = VariableButton(self.quick_text_widget)
        self.btn_phone_numbers.setMinimumSize(QtCore.QSize(80, 0))
        self.btn_phone_numbers.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_phone_numbers.setStyleSheet("")
        self.btn_phone_numbers.setObjectName("btn_phone_numbers")
        self.gridLayout_2.addWidget(self.btn_phone_numbers, 2, 2, 1, 1)
        self.btn_variables = VariableButton(self.quick_text_widget)
        self.btn_variables.setMaximumSize(QtCore.QSize(71, 16777215))
        self.btn_variables.setObjectName("btn_variables")
        self.gridLayout_2.addWidget(self.btn_variables, 2, 3, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_preview = QtWidgets.QLabel(self.quick_text_widget)
        self.lbl_preview.setObjectName("lbl_preview")
        self.gridLayout.addWidget(self.lbl_preview, 0, 0, 1, 1)
        self.ent_preview = QtWidgets.QTextEdit(self.quick_text_widget)
        self.ent_preview.setMaximumSize(QtCore.QSize(800, 16777215))
        self.ent_preview.setObjectName("ent_preview")
        self.gridLayout.addWidget(self.ent_preview, 1, 0, 1, 2)
        self.btn_send_message = QtWidgets.QPushButton(self.quick_text_widget)
        self.btn_send_message.setMaximumSize(QtCore.QSize(71, 16777215))
        self.btn_send_message.setObjectName("btn_send_message")
        self.gridLayout.addWidget(self.btn_send_message, 2, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.gridLayout_5.setColumnStretch(0, 2)
        self.gridLayout_5.setColumnStretch(1, 3)
        self.stacked_frame.addWidget(self.quick_text_widget)
        self.messages_widget = QtWidgets.QWidget()
        self.messages_widget.setObjectName("messages_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.messages_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tbl_messages = CsvTable(self.messages_widget)
        self.tbl_messages.setObjectName("tbl_messages")
        self.tbl_messages.setColumnCount(0)
        self.tbl_messages.setRowCount(0)
        self.horizontalLayout.addWidget(self.tbl_messages)
        self.stacked_frame.addWidget(self.messages_widget)
        self.gridLayout_4.addWidget(self.stacked_frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.action_load_csv = QtWidgets.QAction(MainWindow)
        self.action_load_csv.setObjectName("action_load_csv")
        self.action_close = QtWidgets.QAction(MainWindow)
        self.action_close.setObjectName("action_close")
        self.menuFile.addAction(self.action_load_csv)
        self.menuFile.addAction(self.action_close)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_refresh.setText(_translate("MainWindow", "Refresh"))
        self.btn_csv_input.setText(_translate("MainWindow", "Load CSV"))
        self.lbl_text.setText(_translate("MainWindow", "Text"))
        self.btn_phone_numbers.setText(_translate("MainWindow", "Phone Numbers"))
        self.btn_variables.setText(_translate("MainWindow", "Variables"))
        self.lbl_preview.setText(_translate("MainWindow", "Preview"))
        self.btn_send_message.setText(_translate("MainWindow", "Send"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.action_load_csv.setText(_translate("MainWindow", "Load CSV"))
        self.action_close.setText(_translate("MainWindow", "Close"))
from models.ui import CsvTable, Textbox, VariableButton
