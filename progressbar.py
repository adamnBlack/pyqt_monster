from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
import requests
import var
from p_gui import Ui_Dialog
import os, sys
import time
from imap import delete_email
from PyQt5.QtCore import pyqtSignal, QObject
from fake_useragent import UserAgent

cancel = False
total_email_count = 0

class Communicate(QObject):
    s = pyqtSignal(int)

class Download(Ui_Dialog):
    def __init__(self, dialog, name, link, size, path):
        Ui_Dialog.__init__(self)
        self.setupUi(dialog)
        self.dialog = dialog
        set_icon(self.dialog)
        self.signal = Communicate()
        self.signal.s.connect(self.update_gui)
        self.name = name
        self.link = link
        self.size = size
        self.size_in_kb = int(round(size/1024))
        self.file_path = path
        self.pushButton_cancel.clicked.connect(self.cancel)
        self.label_status.setText("Dowloaded  {} of {} kb".format(0, self.size_in_kb))
        Thread(target=self.download, daemon=True).start()

    def update_gui(self, dowloaded):
        self.label_status.setText("Dowloaded  {} of {} kb".format(dowloaded, self.size_in_kb))
        value = (dowloaded/self.size_in_kb)*100
        self.progressBar.setValue(value)

    def cancel(self):
        global cancel
        cancel = True
        self.dialog.accept()

    def download(self):
        global cancel
        try:
            # ua = UserAgent()
            # userAgent = ua.random
            headers = {'user-agent': 'Wget/1.16 (linux-gnu)'}
            # headers = {'user-agent': '{}'.format(userAgent)}
            # print(headers)
            filepath = "{}/GMonster{}.zip".format(self.file_path, self.name)
            print(filepath)
            url = var.api + "verify/version/download/{}".format(self.name)
            response = requests.post(url, timeout=10)
            data = response.json()
            print(data)
            url = self.link
            r = requests.get(url, stream=True, headers=headers)
            downloaded = 0
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        if cancel==True:
                            break
                        downloaded+=len(chunk)
                        print("Dowloaded {}/{}".format(downloaded, self.size), end='\r')
                        self.signal.s.emit(int(round(downloaded/1024)))
                        f.write(chunk)
            print("download finished")
        except Exception as e:
            print("Error at download update: {}".format(e))


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