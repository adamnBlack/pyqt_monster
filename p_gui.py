# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/progressbar.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 156)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        Dialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_status = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.label_status.setFont(font)
        self.label_status.setText("")
        self.label_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_status.setObjectName("label_status")
        self.gridLayout.addWidget(self.label_status, 0, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.pushButton_cancel.setFont(font)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.gridLayout.addWidget(self.pushButton_cancel, 2, 0, 1, 1, QtCore.Qt.AlignHCenter)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "GMonster"))
        self.pushButton_cancel.setText(_translate("Dialog", "CANCEL"))
