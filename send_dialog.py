from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
import var
from email_input_gui import Ui_Dialog
import os, sys
import time
from smtp import forward, test
import re

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def check(email):
    # pass the regular expression
    # and the string in search() method
    if(re.search(regex,email)):
        return True
    else:
        return False

def set_icon(obj):
    try:
        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)

        p = resource_path('icons/icon.ico')
        obj.setWindowIcon(QtGui.QIcon(p))
    except Exception as e:
        print(e)

class Send(Ui_Dialog):
    def __init__(self, dialog, parent='forward'):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)
        self.dialog = dialog
        set_icon(self.dialog)
        self.type = parent
        self.pushButton_send.clicked.connect(self.thread_starter)
        if self.type=='forward':
            self.label_linedit.setText("Forward To:")
        else:
            self.label_linedit.setText("Send Test To:")
    def thread_starter(self):
        if self.type=='forward':
            Thread(target=self.forward, daemon=True).start()
        else:
            Thread(target=self.test, daemon=True).start()

    def forward(self):
        forward_to = self.lineEdit_email.text().strip()
        self.progressBar.setValue(0)
        if check(forward_to):
            self.label_status.setText("Sending...")
            if forward(forward_to):
                self.label_status.setText("Sent!!!")
                self.progressBar.setValue(100)
            else:
                self.label_status.setText("Error happened while sending!!!")
        else:
            self.label_status.setText("Enter a proper email address...")

    def test(self):
        send_to = self.lineEdit_email.text().strip()
        self.progressBar.setValue(0)
        if check(send_to):
            self.label_status.setText("Sending...")
            if test(send_to):
                self.label_status.setText("Sent!!!")
                self.progressBar.setValue(100)
            else:
                self.label_status.setText("Error happened while sending!!!")
        else:
            self.label_status.setText("Enter a proper email address...")