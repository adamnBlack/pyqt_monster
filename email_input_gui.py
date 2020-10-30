# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/email_input.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 149)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_linedit = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.label_linedit.setFont(font)
        self.label_linedit.setAlignment(QtCore.Qt.AlignCenter)
        self.label_linedit.setObjectName("label_linedit")
        self.gridLayout.addWidget(self.label_linedit, 0, 0, 1, 1)
        self.lineEdit_email = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.lineEdit_email.setFont(font)
        self.lineEdit_email.setFrame(False)
        self.lineEdit_email.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_email.setClearButtonEnabled(True)
        self.lineEdit_email.setObjectName("lineEdit_email")
        self.gridLayout.addWidget(self.lineEdit_email, 0, 1, 1, 2)
        self.pushButton_send = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.pushButton_send.setFont(font)
        self.pushButton_send.setStyleSheet("QPushButton {\n"
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
        self.pushButton_send.setObjectName("pushButton_send")
        self.gridLayout.addWidget(self.pushButton_send, 2, 1, 1, 1)
        self.label_status = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.label_status.setFont(font)
        self.label_status.setText("")
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setObjectName("label_status")
        self.gridLayout.addWidget(self.label_status, 3, 0, 1, 3)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "GMonster"))
        self.label_linedit.setText(_translate("Dialog", "Forward To:"))
        self.pushButton_send.setText(_translate("Dialog", "SEND"))
