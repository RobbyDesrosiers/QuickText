# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\setup_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SetupWindow(object):
    def setupUi(self, SetupWindow):
        SetupWindow.setObjectName("SetupWindow")
        SetupWindow.resize(391, 122)
        SetupWindow.setMinimumSize(QtCore.QSize(0, 0))
        SetupWindow.setMaximumSize(QtCore.QSize(400, 200))
        self.ent_account_sid = QtWidgets.QLineEdit(SetupWindow)
        self.ent_account_sid.setGeometry(QtCore.QRect(110, 24, 271, 20))
        self.ent_account_sid.setObjectName("ent_account_sid")
        self.ent_auth_token = QtWidgets.QLineEdit(SetupWindow)
        self.ent_auth_token.setGeometry(QtCore.QRect(110, 60, 271, 20))
        self.ent_auth_token.setObjectName("ent_auth_token")
        self.btn_account_sid = QtWidgets.QLabel(SetupWindow)
        self.btn_account_sid.setGeometry(QtCore.QRect(110, 9, 141, 16))
        self.btn_account_sid.setObjectName("btn_account_sid")
        self.lbl_auth_token = QtWidgets.QLabel(SetupWindow)
        self.lbl_auth_token.setGeometry(QtCore.QRect(110, 45, 141, 16))
        self.lbl_auth_token.setObjectName("lbl_auth_token")
        self.btn_submit = QtWidgets.QPushButton(SetupWindow)
        self.btn_submit.setGeometry(QtCore.QRect(310, 90, 71, 23))
        self.btn_submit.setObjectName("btn_submit")
        self.btn_cancel = QtWidgets.QPushButton(SetupWindow)
        self.btn_cancel.setGeometry(QtCore.QRect(230, 90, 71, 23))
        self.btn_cancel.setObjectName("btn_cancel")
        self.label = QtWidgets.QLabel(SetupWindow)
        self.label.setGeometry(QtCore.QRect(14, 10, 81, 81))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(".\\ui\\twilio_logo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.check_test_mode = QtWidgets.QCheckBox(SetupWindow)
        self.check_test_mode.setGeometry(QtCore.QRect(150, 95, 70, 17))
        self.check_test_mode.setObjectName("check_test_mode")

        self.retranslateUi(SetupWindow)
        QtCore.QMetaObject.connectSlotsByName(SetupWindow)

    def retranslateUi(self, SetupWindow):
        _translate = QtCore.QCoreApplication.translate
        SetupWindow.setWindowTitle(_translate("SetupWindow", "Form"))
        self.btn_account_sid.setText(_translate("SetupWindow", "Twilio Account SID"))
        self.lbl_auth_token.setText(_translate("SetupWindow", "Twilio Auth Token"))
        self.btn_submit.setText(_translate("SetupWindow", "Submit"))
        self.btn_cancel.setText(_translate("SetupWindow", "Cancel"))
        self.check_test_mode.setText(_translate("SetupWindow", "Test Mode"))
