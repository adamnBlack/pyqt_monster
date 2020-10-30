# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1405, 1053)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: #E3E3E3;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_inbox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_inbox.sizePolicy().hasHeightForWidth())
        self.groupBox_inbox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_inbox.setFont(font)
        self.groupBox_inbox.setStyleSheet("background-color: #E3E3E3;")
        self.groupBox_inbox.setTitle("")
        self.groupBox_inbox.setObjectName("groupBox_inbox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_inbox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidget_inbox = QtWidgets.QTableWidget(self.groupBox_inbox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.tableWidget_inbox.setFont(font)
        self.tableWidget_inbox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"selection-color: #79d70f;")
        self.tableWidget_inbox.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tableWidget_inbox.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_inbox.setShowGrid(False)
        self.tableWidget_inbox.setObjectName("tableWidget_inbox")
        self.tableWidget_inbox.setColumnCount(4)
        self.tableWidget_inbox.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_inbox.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_inbox.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_inbox.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_inbox.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_inbox.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_inbox.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_inbox.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        item.setFont(font)
        self.tableWidget_inbox.setItem(0, 2, item)
        self.tableWidget_inbox.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_inbox.horizontalHeader().setDefaultSectionSize(125)
        self.tableWidget_inbox.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.tableWidget_inbox, 8, 0, 1, 6)
        self.label_5 = QtWidgets.QLabel(self.groupBox_inbox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_email_status = QtWidgets.QLabel(self.groupBox_inbox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.label_email_status.setFont(font)
        self.label_email_status.setText("")
        self.label_email_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_email_status.setObjectName("label_email_status")
        self.gridLayout_2.addWidget(self.label_email_status, 9, 2, 1, 4)
        self.pushButton_delete = QtWidgets.QPushButton(self.groupBox_inbox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.setStyleSheet("QPushButton {\n"
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
        self.pushButton_delete.setObjectName("pushButton_delete")
        self.gridLayout_2.addWidget(self.pushButton_delete, 9, 1, 1, 1)
        self.radioButton_group_a = QtWidgets.QRadioButton(self.groupBox_inbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_group_a.sizePolicy().hasHeightForWidth())
        self.radioButton_group_a.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.radioButton_group_a.setFont(font)
        self.radioButton_group_a.setStyleSheet("")
        self.radioButton_group_a.setCheckable(True)
        self.radioButton_group_a.setChecked(True)
        self.radioButton_group_a.setAutoExclusive(True)
        self.radioButton_group_a.setObjectName("radioButton_group_a")
        self.gridLayout_2.addWidget(self.radioButton_group_a, 2, 0, 1, 1)
        self.pushButton_load_db = QtWidgets.QPushButton(self.groupBox_inbox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.pushButton_load_db.setFont(font)
        self.pushButton_load_db.setStyleSheet("QPushButton {\n"
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
        self.pushButton_load_db.setObjectName("pushButton_load_db")
        self.gridLayout_2.addWidget(self.pushButton_load_db, 9, 0, 1, 1)
        self.radioButton_group_b = QtWidgets.QRadioButton(self.groupBox_inbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioButton_group_b.sizePolicy().hasHeightForWidth())
        self.radioButton_group_b.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.radioButton_group_b.setFont(font)
        self.radioButton_group_b.setStyleSheet("")
        self.radioButton_group_b.setCheckable(True)
        self.radioButton_group_b.setAutoExclusive(True)
        self.radioButton_group_b.setObjectName("radioButton_group_b")
        self.gridLayout_2.addWidget(self.radioButton_group_b, 3, 0, 1, 1)
        self.dateEdit_imap_since = QtWidgets.QDateEdit(self.groupBox_inbox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.dateEdit_imap_since.setFont(font)
        self.dateEdit_imap_since.setStyleSheet("color: rgb(0, 0, 0);\n"
"background-color: rgb(255, 255, 255);")
        self.dateEdit_imap_since.setWrapping(True)
        self.dateEdit_imap_since.setFrame(True)
        self.dateEdit_imap_since.setAlignment(QtCore.Qt.AlignCenter)
        self.dateEdit_imap_since.setReadOnly(False)
        self.dateEdit_imap_since.setProperty("showGroupSeparator", False)
        self.dateEdit_imap_since.setCalendarPopup(True)
        self.dateEdit_imap_since.setObjectName("dateEdit_imap_since")
        self.gridLayout_2.addWidget(self.dateEdit_imap_since, 2, 1, 1, 1)
        self.pushButton_download_email = QtWidgets.QPushButton(self.groupBox_inbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_download_email.sizePolicy().hasHeightForWidth())
        self.pushButton_download_email.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_download_email.setFont(font)
        self.pushButton_download_email.setStyleSheet("QPushButton {\n"
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
        self.pushButton_download_email.setObjectName("pushButton_download_email")
        self.gridLayout_2.addWidget(self.pushButton_download_email, 3, 1, 1, 1)
        self.pushButton_cancel_email = QtWidgets.QPushButton(self.groupBox_inbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_cancel_email.sizePolicy().hasHeightForWidth())
        self.pushButton_cancel_email.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_cancel_email.setFont(font)
        self.pushButton_cancel_email.setStyleSheet("QPushButton {\n"
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
        self.pushButton_cancel_email.setObjectName("pushButton_cancel_email")
        self.gridLayout_2.addWidget(self.pushButton_cancel_email, 3, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox_inbox, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setStyleSheet("background-color: #E3E3E3;")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label = QtWidgets.QLabel(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout_6.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_original_recipient = QtWidgets.QLineEdit(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_original_recipient.sizePolicy().hasHeightForWidth())
        self.lineEdit_original_recipient.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.lineEdit_original_recipient.setFont(font)
        self.lineEdit_original_recipient.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_original_recipient.setFrame(False)
        self.lineEdit_original_recipient.setReadOnly(True)
        self.lineEdit_original_recipient.setClearButtonEnabled(True)
        self.lineEdit_original_recipient.setObjectName("lineEdit_original_recipient")
        self.gridLayout_6.addWidget(self.lineEdit_original_recipient, 0, 1, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_5, 1, 0, 1, 1)
        self.textBrowser_compose = QtWidgets.QTextBrowser(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.textBrowser_compose.setFont(font)
        self.textBrowser_compose.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textBrowser_compose.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser_compose.setReadOnly(False)
        self.textBrowser_compose.setObjectName("textBrowser_compose")
        self.gridLayout_3.addWidget(self.textBrowser_compose, 7, 0, 1, 1)
        self.groupBox_8 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_8.setTitle("")
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_8)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_4 = QtWidgets.QLabel(self.groupBox_8)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_10.addWidget(self.label_4, 9, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.label_3 = QtWidgets.QLabel(self.groupBox_8)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_10.addWidget(self.label_3, 0, 0, 1, 1)
        self.lineEdit_subject = QtWidgets.QLineEdit(self.groupBox_8)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.lineEdit_subject.setFont(font)
        self.lineEdit_subject.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_subject.setFrame(False)
        self.lineEdit_subject.setClearButtonEnabled(True)
        self.lineEdit_subject.setObjectName("lineEdit_subject")
        self.gridLayout_10.addWidget(self.lineEdit_subject, 9, 1, 1, 4)
        self.pushButton_attachments = QtWidgets.QPushButton(self.groupBox_8)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_attachments.setFont(font)
        self.pushButton_attachments.setStyleSheet("QPushButton {\n"
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
        self.pushButton_attachments.setObjectName("pushButton_attachments")
        self.gridLayout_10.addWidget(self.pushButton_attachments, 0, 4, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_8, 6, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(50)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.radioButton_reply = QtWidgets.QRadioButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton_reply.setFont(font)
        self.radioButton_reply.setChecked(False)
        self.radioButton_reply.setObjectName("radioButton_reply")
        self.gridLayout_7.addWidget(self.radioButton_reply, 0, 0, 1, 1)
        self.radioButton_send_campaign = QtWidgets.QRadioButton(self.groupBox_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton_send_campaign.setFont(font)
        self.radioButton_send_campaign.setChecked(True)
        self.radioButton_send_campaign.setObjectName("radioButton_send_campaign")
        self.gridLayout_7.addWidget(self.radioButton_send_campaign, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_3, 2, 0, 1, 1)
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_6.setTitle("")
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.lineEdit_num_per_address = QtWidgets.QLineEdit(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_num_per_address.sizePolicy().hasHeightForWidth())
        self.lineEdit_num_per_address.setSizePolicy(sizePolicy)
        self.lineEdit_num_per_address.setMinimumSize(QtCore.QSize(140, 24))
        self.lineEdit_num_per_address.setMaximumSize(QtCore.QSize(140, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.lineEdit_num_per_address.setFont(font)
        self.lineEdit_num_per_address.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_num_per_address.setMaxLength(4)
        self.lineEdit_num_per_address.setFrame(False)
        self.lineEdit_num_per_address.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_num_per_address.setObjectName("lineEdit_num_per_address")
        self.gridLayout_8.addWidget(self.lineEdit_num_per_address, 1, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_6 = QtWidgets.QLabel(self.groupBox_6)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_8.addWidget(self.label_6, 0, 1, 1, 1)
        self.radioButton_campaign_group_a = QtWidgets.QRadioButton(self.groupBox_6)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton_campaign_group_a.setFont(font)
        self.radioButton_campaign_group_a.setChecked(True)
        self.radioButton_campaign_group_a.setObjectName("radioButton_campaign_group_a")
        self.gridLayout_8.addWidget(self.radioButton_campaign_group_a, 3, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.label_2 = QtWidgets.QLabel(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_8.addWidget(self.label_2, 1, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.label_delay_between_emails = QtWidgets.QLabel(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_delay_between_emails.sizePolicy().hasHeightForWidth())
        self.label_delay_between_emails.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_delay_between_emails.setFont(font)
        self.label_delay_between_emails.setObjectName("label_delay_between_emails")
        self.gridLayout_8.addWidget(self.label_delay_between_emails, 2, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.radioButton_campaign_group_b = QtWidgets.QRadioButton(self.groupBox_6)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.radioButton_campaign_group_b.setFont(font)
        self.radioButton_campaign_group_b.setObjectName("radioButton_campaign_group_b")
        self.gridLayout_8.addWidget(self.radioButton_campaign_group_b, 3, 2, 1, 1, QtCore.Qt.AlignLeft)
        self.lineEdit_delay_between_emails = QtWidgets.QLineEdit(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_delay_between_emails.sizePolicy().hasHeightForWidth())
        self.lineEdit_delay_between_emails.setSizePolicy(sizePolicy)
        self.lineEdit_delay_between_emails.setMinimumSize(QtCore.QSize(140, 24))
        self.lineEdit_delay_between_emails.setMaximumSize(QtCore.QSize(140, 24))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.lineEdit_delay_between_emails.setFont(font)
        self.lineEdit_delay_between_emails.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_delay_between_emails.setMaxLength(5)
        self.lineEdit_delay_between_emails.setFrame(False)
        self.lineEdit_delay_between_emails.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_delay_between_emails.setObjectName("lineEdit_delay_between_emails")
        self.gridLayout_8.addWidget(self.lineEdit_delay_between_emails, 2, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.gridLayout_4.addWidget(self.groupBox_6, 2, 1, 1, 1)
        self.comboBox_attachments = QtWidgets.QComboBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.comboBox_attachments.setFont(font)
        self.comboBox_attachments.setFrame(False)
        self.comboBox_attachments.setObjectName("comboBox_attachments")
        self.gridLayout_4.addWidget(self.comboBox_attachments, 3, 0, 1, 2)
        self.pushButton_attachments_clear = QtWidgets.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.pushButton_attachments_clear.setFont(font)
        self.pushButton_attachments_clear.setStyleSheet("QPushButton {\n"
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
        self.pushButton_attachments_clear.setObjectName("pushButton_attachments_clear")
        self.gridLayout_4.addWidget(self.pushButton_attachments_clear, 3, 2, 1, 1, QtCore.Qt.AlignRight)
        self.gridLayout_3.addWidget(self.groupBox_2, 4, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.pushButton_proxy_provider = QtWidgets.QPushButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_proxy_provider.sizePolicy().hasHeightForWidth())
        self.pushButton_proxy_provider.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_proxy_provider.setFont(font)
        self.pushButton_proxy_provider.setStyleSheet("QPushButton {\n"
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
        self.pushButton_proxy_provider.setFlat(False)
        self.pushButton_proxy_provider.setObjectName("pushButton_proxy_provider")
        self.gridLayout_5.addWidget(self.pushButton_proxy_provider, 0, 2, 1, 1)
        self.pushButton_gmail_provider = QtWidgets.QPushButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_gmail_provider.sizePolicy().hasHeightForWidth())
        self.pushButton_gmail_provider.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_gmail_provider.setFont(font)
        self.pushButton_gmail_provider.setStyleSheet("QPushButton {\n"
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
        self.pushButton_gmail_provider.setFlat(False)
        self.pushButton_gmail_provider.setObjectName("pushButton_gmail_provider")
        self.gridLayout_5.addWidget(self.pushButton_gmail_provider, 0, 1, 1, 1)
        self.pushButton_email_scraper = QtWidgets.QPushButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_email_scraper.sizePolicy().hasHeightForWidth())
        self.pushButton_email_scraper.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_email_scraper.setFont(font)
        self.pushButton_email_scraper.setStyleSheet("QPushButton {\n"
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
        self.pushButton_email_scraper.setFlat(False)
        self.pushButton_email_scraper.setObjectName("pushButton_email_scraper")
        self.gridLayout_5.addWidget(self.pushButton_email_scraper, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_4, 0, 0, 1, 2)
        self.groupBox_7 = QtWidgets.QGroupBox(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.groupBox_7.setFont(font)
        self.groupBox_7.setTitle("")
        self.groupBox_7.setObjectName("groupBox_7")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_7)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.pushButton_clear_compose = QtWidgets.QPushButton(self.groupBox_7)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        self.pushButton_clear_compose.setFont(font)
        self.pushButton_clear_compose.setStyleSheet("QPushButton {\n"
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
        self.pushButton_clear_compose.setObjectName("pushButton_clear_compose")
        self.gridLayout_9.addWidget(self.pushButton_clear_compose, 0, 7, 1, 1, QtCore.Qt.AlignRight)
        self.label_send_email_status = QtWidgets.QLabel(self.groupBox_7)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.label_send_email_status.setFont(font)
        self.label_send_email_status.setText("")
        self.label_send_email_status.setAlignment(QtCore.Qt.AlignCenter)
        self.label_send_email_status.setObjectName("label_send_email_status")
        self.gridLayout_9.addWidget(self.label_send_email_status, 1, 0, 1, 2)
        self.pushButton_send = QtWidgets.QPushButton(self.groupBox_7)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
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
        self.gridLayout_9.addWidget(self.pushButton_send, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.pushButton_send_cancel = QtWidgets.QPushButton(self.groupBox_7)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_send_cancel.setFont(font)
        self.pushButton_send_cancel.setStyleSheet("QPushButton {\n"
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
        self.pushButton_send_cancel.setObjectName("pushButton_send_cancel")
        self.gridLayout_9.addWidget(self.pushButton_send_cancel, 0, 1, 1, 1, QtCore.Qt.AlignLeft)
        self.gridLayout_3.addWidget(self.groupBox_7, 8, 0, 1, 1)
        self.textBrowser_show_email = QtWidgets.QTextBrowser(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(13)
        self.textBrowser_show_email.setFont(font)
        self.textBrowser_show_email.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textBrowser_show_email.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser_show_email.setObjectName("textBrowser_show_email")
        self.gridLayout_3.addWidget(self.textBrowser_show_email, 2, 0, 1, 1)
        self.progressBar_send_email = QtWidgets.QProgressBar(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.progressBar_send_email.setFont(font)
        self.progressBar_send_email.setProperty("value", 0)
        self.progressBar_send_email.setObjectName("progressBar_send_email")
        self.gridLayout_3.addWidget(self.progressBar_send_email, 9, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setStyleSheet("image: url(:/newPrefix/software logo.png);")
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GMonster"))
        item = self.tableWidget_inbox.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "FROM"))
        item = self.tableWidget_inbox.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "SUBJECT"))
        __sortingEnabled = self.tableWidget_inbox.isSortingEnabled()
        self.tableWidget_inbox.setSortingEnabled(False)
        self.tableWidget_inbox.setSortingEnabled(__sortingEnabled)
        self.label_5.setText(_translate("MainWindow", "ADDRESS GROUP"))
        self.pushButton_delete.setText(_translate("MainWindow", "DELETE"))
        self.radioButton_group_a.setText(_translate("MainWindow", "Group A"))
        self.pushButton_load_db.setText(_translate("MainWindow", "LOAD DB"))
        self.radioButton_group_b.setText(_translate("MainWindow", "Group B"))
        self.pushButton_download_email.setText(_translate("MainWindow", "DOWNLOAD"))
        self.pushButton_cancel_email.setText(_translate("MainWindow", "CANCEL"))
        self.label.setText(_translate("MainWindow", "ORIGINAL RECIPIENT:"))
        self.label_4.setText(_translate("MainWindow", "SUBJECT:"))
        self.label_3.setText(_translate("MainWindow", "COMPOSE"))
        self.pushButton_attachments.setText(_translate("MainWindow", "ATTACHMENTS"))
        self.radioButton_reply.setText(_translate("MainWindow", "Reply"))
        self.radioButton_send_campaign.setText(_translate("MainWindow", "Send Campaign"))
        self.lineEdit_num_per_address.setPlaceholderText(_translate("MainWindow", "ENTER NUMBER"))
        self.label_6.setText(_translate("MainWindow", "CAMPAIGN SETTINGS"))
        self.radioButton_campaign_group_a.setText(_translate("MainWindow", "Group A"))
        self.label_2.setText(_translate("MainWindow", "NUM EMAILS PER ACCOUNT"))
        self.label_delay_between_emails.setText(_translate("MainWindow", "DELAY BETWEEN EMAILS"))
        self.radioButton_campaign_group_b.setText(_translate("MainWindow", "Group B"))
        self.lineEdit_delay_between_emails.setText(_translate("MainWindow", "5-20"))
        self.lineEdit_delay_between_emails.setPlaceholderText(_translate("MainWindow", "Enter a Range"))
        self.pushButton_attachments_clear.setText(_translate("MainWindow", "CLEAR"))
        self.pushButton_proxy_provider.setText(_translate("MainWindow", "GMonster Proxies"))
        self.pushButton_gmail_provider.setText(_translate("MainWindow", "Custom \n"
"Gmail Accounts"))
        self.pushButton_email_scraper.setText(_translate("MainWindow", "Targeted \n"
"Email Leads"))
        self.pushButton_clear_compose.setText(_translate("MainWindow", "CLEAR"))
        self.pushButton_send.setText(_translate("MainWindow", "SEND"))
        self.pushButton_send_cancel.setText(_translate("MainWindow", "CANCEL"))
import logo_rc
