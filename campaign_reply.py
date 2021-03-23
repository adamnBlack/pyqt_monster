from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
import requests
import var
from p_gui import Ui_Dialog
import os, sys
import time
from PyQt5.QtCore import pyqtSignal, QObject
from pyautogui import alert, password, confirm


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

class Reply(Ui_Dialog):
    def __init__(self, dialog):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)
        self.dialog = dialog
        set_icon(self.dialog)
        self.pushButton_cancel.clicked.connect(self.cancel)

        Thread(target=self.reply, daemon=True).start()

    def reply(self):
        self.label_status.setText("Replying...")
        from smtp import reply
        
        result = reply()
        if result == 1:
            self.label_status.setText("Replying Succesful")
            self.progressBar.setValue(100)
            
        else:
            self.label_status.setText("Replying Failed!!!")
        
        self.pushButton_cancel.setText("Close")

    def cancel(self):
        self.dialog.accept()


class Campaign(Ui_Dialog):
    def __init__(self, dialog, group=None, delay_start=None, delay_end=None, total_email_to_be_sent=None):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)
        self.dialog = dialog
        set_icon(self.dialog)
        
        self.pushButton_cancel.clicked.connect(self.cancel)
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_gui)
        
        self.group = group
        self.delay_start = delay_start
        self.delay_end = delay_end
        self.total_email_to_be_sent = total_email_to_be_sent

        from smtp import main

        Thread(target=main, daemon=True, args=[self.group, self.delay_start, self.delay_end]).start()
        self.timer.start()
    
    def update_gui(self):
        try:
            if var.send_campaign_run_status == False:
                if var.stop_send_campaign == True:
                    self.label_status.setText(f"Sending Cancelled : {var.send_campaign_email_count}/{self.total_email_to_be_sent} Accounts Failed : {var.email_failed}")
                else:
                    self.label_status.setText(f"Sending Finished : {var.send_campaign_email_count}/{self.total_email_to_be_sent} Accounts Failed : {var.email_failed}")
                self.pushButton_cancel.setText("Close")
            else:
                value = (var.send_campaign_email_count/self.total_email_to_be_sent)*100
                self.label_status.setText(f"Total Email Sent : {var.send_campaign_email_count}/{self.total_email_to_be_sent}")
                self.progressBar.setValue(value)
        except Exception as e:
            print("Error at campaign_reply.Campaign.update_gui : {}".format(e))

    def cancel(self):
        var.stop_send_campaign = True
        self.dialog.accept()