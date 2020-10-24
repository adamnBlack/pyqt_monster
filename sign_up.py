# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/sign_up.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 190)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        Dialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.pushButton_sign_up = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.pushButton_sign_up.setFont(font)
        self.pushButton_sign_up.setStyleSheet("QPushButton {\n"
"    border: 1px solid #555;\n"
"    border-radius: 3px;\n"
"    border-style: Solid;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #e5e5e5, stop: 1 #4B7DAD\n"
"        );\n"
"    padding: 5px 28px;\n"
"    color: rgb(255, 255, 255);\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #e5e5e5, stop: 1 #709fb0\n"
"        );\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #e5e5e5, stop: 1 #79d70f\n"
"        );\n"
"    }")
        self.pushButton_sign_up.setObjectName("pushButton_sign_up")
        self.gridLayout.addWidget(self.pushButton_sign_up, 3, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.lineEdit_email = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_email.setMaxLength(64)
        self.lineEdit_email.setFrame(False)
        self.lineEdit_email.setClearButtonEnabled(True)
        self.lineEdit_email.setObjectName("lineEdit_email")
        self.gridLayout.addWidget(self.lineEdit_email, 0, 1, 1, 1)
        self.lineEdit_password = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_password.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.lineEdit_password.setMaxLength(20)
        self.lineEdit_password.setFrame(False)
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setClearButtonEnabled(True)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.gridLayout.addWidget(self.lineEdit_password, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.lineEdit_confirm_password = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_confirm_password.setMaxLength(20)
        self.lineEdit_confirm_password.setFrame(False)
        self.lineEdit_confirm_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_confirm_password.setClearButtonEnabled(True)
        self.lineEdit_confirm_password.setObjectName("lineEdit_confirm_password")
        self.gridLayout.addWidget(self.lineEdit_confirm_password, 2, 1, 1, 1)
        self.label_status = QtWidgets.QLabel(Dialog)
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setWordWrap(True)
        self.label_status.setObjectName("label_status")
        self.gridLayout.addWidget(self.label_status, 4, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "GMonster"))
        self.label_2.setText(_translate("Dialog", "Password"))
        self.pushButton_sign_up.setText(_translate("Dialog", "Sign Up"))
        self.label.setText(_translate("Dialog", "Email"))
        self.label_3.setText(_translate("Dialog", "Confirm Password"))
        self.label_status.setText(_translate("Dialog", "Password must be equal to or more than 8 characters"))
