from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
import var
from p_gui import Ui_Dialog
import os, sys
import time
from imap import delete_email

cancel = False
total_email_count = 0

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

class Delete_email(Ui_Dialog):
    def __init__(self, dialog):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)
        self.dialog = dialog
        set_icon(self.dialog)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.progressbar)
        self.pushButton_cancel.clicked.connect(self.cancel_delete)
        Thread(target=thread_starter, daemon=True).start()
        self.timer.start()

    def cancel_delete(self):
        var.stop_delete = True
        self.timer.stop()

    def progressbar(self):
        global total_email_count
        if total_email_count != 0:
            value = (var.delete_email_count/total_email_count)*100
            self.label_status.setText("Deleted : {}/{}".format(var.delete_email_count, total_email_count))
            self.progressBar.setValue(value)
        else:
            self.label_status.setText("Preparing for deleting ...")


def thread_starter():
    global total_email_count
    temp_df = var.inbox_data.copy()
    temp_df = temp_df.loc[temp_df['checkbox_status'] == 1]
    total_email_count = len(temp_df)
    temp_df = temp_df.groupby('user')
    var.delete_email_count = 0
    var.stop_delete = False

    for group_name, df_group in temp_df:

        if var.stop_delete == True:
            break

        while var.thread_open >= var.limit_of_thread and var.stop_delete == False:
            time.sleep(1)

        # print('Group name - {}'.format(group_name))
        Thread(target=delete_email, daemon=True, args=(df_group,)).start()
    while var.thread_open!=0 and var.stop_delete == False:
        time.sleep(1)

    for row_index, row in var.inbox_data.iterrows():
        var.email_q.put(row.to_dict().copy())

    print("deleting finished")