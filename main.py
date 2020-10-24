import datetime
from pyautogui import alert, password, confirm
import json
from threading import Thread
from time import sleep
import os
import sys
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow
import encodings.idna
from utils import update_config_json
import pandas as pd
import webbrowser
import subprocess
print("App started....")
# import uuid
# print(uuid.UUID(int=uuid.getnode()))


class MyGui(Ui_MainWindow, QtWidgets.QWidget):
    def __init__(self, mainWindow):
        Ui_MainWindow.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(mainWindow)



class myMainClass():
    def __init__(self):
        GUI.lineEdit_num_per_address.setText(str(var.num_emails_per_address))
        GUI.lineEdit_delay_between_emails.setText(str(var.delay_between_emails))

        self.table_timer = QtCore.QTimer()
        self.table_timer.setInterval(10)
        self.table_timer.timeout.connect(self.add_to_table)

        self.progressbar = QtCore.QTimer()
        self.progressbar.setInterval(1)
        self.progressbar.timeout.connect(self.progressbar_download)

        self.send_progressbar = QtCore.QTimer()
        self.send_progressbar.setInterval(1)
        self.send_progressbar.timeout.connect(self.progressbar_send)

        date = QtCore.QDate.fromString(var.date, "M/d/yyyy")
        GUI.dateEdit_imap_since.setDate(date)
        GUI.dateEdit_imap_since.setMaximumDate(QtCore.QDate.currentDate().addDays(-1))
        GUI.dateEdit_imap_since.dateChanged.connect(self.date_update)

        GUI.pushButton_download_email.clicked.connect(self.downloading_email)
        GUI.pushButton_cancel_email.clicked.connect(self.email_cancel)

        GUI.pushButton_send.clicked.connect(self.send)
        GUI.pushButton_send_cancel.clicked.connect(self.send_cancel)


        GUI.pushButton_cancel_email.setEnabled(False)
        GUI.lineEdit_subject.setText(var.compose_email_subject)
        GUI.textBrowser_compose.setText(var.compose_email_body)

        GUI.pushButton_attachments.clicked.connect(self.openFileNamesDialog)
        GUI.pushButton_attachments_clear.clicked.connect(self.clear_files)
        GUI.pushButton_email_scraper.clicked.connect(self.email_scraper)
        GUI.pushButton_gmail_provider.clicked.connect(self.gmail_provider)
        GUI.pushButton_proxy_provider.clicked.connect(self.proxy_provider)
        GUI.radioButton_reply.clicked.connect(self.change_subject)
        GUI.pushButton_reload_db.clicked.connect(self.reload_db)
        GUI.pushButton_clear_compose.clicked.connect(self.clear_compose)

    def clear_compose(self):
        GUI.textBrowser_compose.clear()

    def reload_db(self):
        Thread(target=var.load_db, daemon=True).start()

    def change_subject(self):
        try:
            subject = var.email_in_view['subject']
            subject = subject if ("RE: " in subject or "Re: " in subject) else "RE: {}".format(subject)
            GUI.lineEdit_subject.setText(subject)
        except Exception as e:
            print("Error while setting subject : {}".format(e))

        # GUI.radioButton_reply.setChecked(True)
    def gmail_provider(self):
        webbrowser.open_new(var.gmail_provider)

    def proxy_provider(self):
        webbrowser.open_new(var.proxy_provider)

    def email_scraper(self):
        webbrowser.open_new(var.email_scraper)

    def clear_files(self):
        var.files = []
        GUI.comboBox_attachments.clear()

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(None,"Attach files", "","All Files (*)", options=options)
        if files:
            var.files = []
            var.files = files
            GUI.comboBox_attachments.clear()
            GUI.comboBox_attachments.addItems(var.files)

    def send(self):
        try:
            var.stop_send_campaign = False
            var.thread_open_campaign = 0
            var.send_campaign_email_count = 0
            if GUI.radioButton_reply.isChecked():
                result = confirm(text='Are you sure?', title='Confirmation Window', buttons=['OK', 'Cancel'])
                if result == 'OK':
                    Thread(target= self.reply, daemon=True).start()
                else:
                    print('cancelled')
            else:
                result = confirm(text='Are you sure?', title='Confirmation Window', buttons=['OK', 'Cancel'])
                if result == 'OK':
                    print("send_campaign")
                    Thread(target= self.send_campaign, daemon=True).start()
                else:
                    print('cancelled')
            GUI.label_send_email_status.setText("Sending...")
            GUI.pushButton_send.setEnabled(False)
            self.send_progressbar.start()
        except:
            pass



    def send_campaign(self):
        var.num_emails_per_address = int(GUI.lineEdit_num_per_address.text())
        var.delay_between_emails = GUI.lineEdit_delay_between_emails.text()
        delay_start = int(var.delay_between_emails.split("-")[0].strip())
        delay_end = int(var.delay_between_emails.split("-")[1].strip())
        update_config_json()
        var.compose_email_subject = GUI.lineEdit_subject.text()
        var.compose_email_body = GUI.textBrowser_compose.toPlainText()
        # batch = len(var.target)/var.num_emails_per_address
        var.group_a['flag'] = 0
        var.group_b['flag'] = 0
        var.target['flag'] = 0
        if GUI.radioButton_campaign_group_a.isChecked():
            print("Group a")
            Thread(target=smtp.main, daemon=True, args=[var.group_a, delay_start, delay_end]).start()
        else:
            print("Group b")
            Thread(target=smtp.main, daemon=True, args=[var.group_b, delay_start, delay_end]).start()

    def reply(self):
        var.email_in_view['subject'] = GUI.lineEdit_subject.text()
        var.email_in_view['body'] = GUI.textBrowser_compose.toPlainText()
        print(var.email_in_view)
        result = smtp.reply()
        if result == 1:
            alert(text='Email sent', title='Alert', button='OK')
        else:
            alert(text='Couldn\'t send', title='Alert', button='OK')

    def send_cancel(self):
        result = confirm(text='Are you sure?', title='Confirmation Window', buttons=['OK', 'Cancel'])
        if result == 'OK':
            var.stop_send_campaign = True
        else:
            var.stop_send_campaign = False

    def progressbar_download(self):
        GUI.progressBar_send_email.setValue((var.acc_finished/var.total_acc)*100)
        if var.acc_finished == var.total_acc:
            GUI.pushButton_download_email.setEnabled(True)
            if var.stop_download == True:
                GUI.pushButton_cancel_email.setEnabled(False)
                GUI.label_email_status.setText("Downloading cancelled")
            else:
                GUI.label_email_status.setText("Downloading finished")
            self.table_timer.start()
            self.progressbar.stop()

    def progressbar_send(self):
        if GUI.radioButton_campaign_group_a.isChecked():
            if len(var.group_a)*var.num_emails_per_address > len(var.target):
                value = (var.send_campaign_email_count/len(var.target))*100
            else:
                value = (var.send_campaign_email_count/(len(var.group_a)*var.num_emails_per_address))*100
        else:
            if len(var.group_b)*var.num_emails_per_address > len(var.target):
                value = (var.send_campaign_email_count/len(var.target))*100
            else:
                value = (var.send_campaign_email_count/(len(var.group_b)*var.num_emails_per_address))*100

        GUI.progressBar_send_email.setValue(value)
        if var.send_campaign_run_status == False:
            GUI.pushButton_send.setEnabled(True)
            print("Sending finished. Stopping timer.")
            if var.stop_send_campaign == True:
                GUI.label_send_email_status.setText("Sending Cancelled")
            else:
                GUI.label_send_email_status.setText("Sending Finished")
            self.send_progressbar.stop()


    def downloading_email(self):
        try:
            update_config_json()
            GUI.pushButton_download_email.setEnabled(False)
            GUI.pushButton_cancel_email.setEnabled(True)
            with var.email_q.mutex:
                var.email_q.queue.clear()
            GUI.label_email_status.setText("Downloading...")
            var.total_email = 0
            var.thread_open = 0
            var.acc_finished = 0
            var.stop_download = False
            self.table_timer.stop()
            var.inbox_data = pd.DataFrame()
            var.row_pos = 0
            GUI.tableWidget_inbox.setRowCount(0)
            if GUI.radioButton_group_a.isChecked():
                print("Group a")
                var.total_acc = len(var.group_a)
                Thread(target=imap.main, daemon=True, args=[var.group_a]).start()
            else:
                print("Group b")
                var.total_acc = len(var.group_b)
                Thread(target=imap.main, daemon=True, args=[var.group_b]).start()

            print("Downloading ...")
            self.progressbar.start()
        except:
            pass

    def start_timer(self):
        self.table_timer.start()

    # def clear_table(self):
    #     result = confirm(text='Are you sure?', title='Confirmation Window', buttons=['OK', 'Cancel'])
    #     if result == 'OK':
    #         print("cleared table")
    #         self.table_timer.stop()
    #         var.inbox_data = pd.DataFrame()
    #         var.row_pos = 0
    #         GUI.tableWidget_inbox.setRowCount(0)
    #     else:
    #         print("cancelled")

    def email_cancel(self):
        result = confirm(text='Are you sure?', title='Confirmation Window', buttons=['OK', 'Cancel'])
        if result == 'OK':
            print("Download Cancel")
            self.table_timer.stop()
            var.stop_download = True
        else:
            print("denined")

    def add_to_table(self):
        count = 0

        while not var.email_q.empty():
            if count == 2:
                break
            row_data = var.email_q.get()

            var.inbox_data = var.inbox_data.append(row_data, ignore_index=True)

            GUI.tableWidget_inbox.setRowCount(var.row_pos+1)

            GUI.tableWidget_inbox.setItem(var.row_pos,1,
                                        QTableWidgetItem(row_data['from']))
            # GUI.tableWidget_inbox.resizeColumnToContents(1)
            GUI.tableWidget_inbox.setItem(var.row_pos,2,
                                        QTableWidgetItem(row_data['subject']))

            button_show_mail = QtWidgets.QPushButton('')
            button_show_mail.setStyleSheet(var.button_style)
            button_show_mail.clicked.connect(self.email_show)
            if row_data['flag'] == 'UNSEEN':
                button_show_mail.setIcon(QtGui.QIcon(var.mail_unread_icon))
            else:
                button_show_mail.setIcon(QtGui.QIcon(var.mail_read_icon))
            GUI.tableWidget_inbox.setCellWidget(var.row_pos, 0, button_show_mail)

            button_delete = QtWidgets.QPushButton('')
            button_delete.setStyleSheet(var.button_style)
            button_delete.clicked.connect(self.email_delete)
            button_delete.setIcon(QtGui.QIcon(var.delete_icon))
            GUI.tableWidget_inbox.setCellWidget(var.row_pos, 3, button_delete)
            GUI.tableWidget_inbox.resizeColumnToContents(0)
            GUI.tableWidget_inbox.resizeColumnToContents(1)
            GUI.tableWidget_inbox.resizeColumnToContents(3)
            var.row_pos+=1
            count+=1
        else:
            self.table_timer.stop()
            GUI.label_email_status.setText("Showing Finished")
            print("finished")

    def email_show(self):
        print('email showed')
        row, column = self.get_index_of_button(GUI.tableWidget_inbox)
        Thread(target=imap.set_read_flag, daemon=True, args=[row,]).start()
        button_show_mail = QtWidgets.QPushButton('')
        button_show_mail.setStyleSheet(var.button_style)
        button_show_mail.clicked.connect(self.email_show)
        button_show_mail.setIcon(QtGui.QIcon(var.mail_read_icon))
        GUI.tableWidget_inbox.setCellWidget(row, 0, button_show_mail)

        GUI.lineEdit_original_recipient.setText(var.inbox_data['to'][row])
        # print(var.inbox_data['body'][row])
        var.email_in_view = {
                    'uid': var.inbox_data['uid'][row],
                    'to_mail': var.inbox_data['to_mail'][row],
                    'message-id': var.inbox_data['message-id'][row],
                    'from_mail': var.inbox_data['from_mail'][row],
                    'subject': var.inbox_data['subject'][row],
                    'user': var.inbox_data['user'][row],
                    'pass': var.inbox_data['pass'][row],
                    'proxy_host': var.inbox_data['proxy_host'][row],
                    'proxy_port': var.inbox_data['proxy_port'][row],
                    'proxy_user': var.inbox_data['proxy_user'][row],
                    'proxy_pass': var.inbox_data['proxy_pass'][row],
                    'FIRSTFROMNAME': var.inbox_data['FIRSTFROMNAME'][row],
                    'LASTFROMNAME': var.inbox_data['LASTFROMNAME'][row]
                    }
        if GUI.radioButton_reply.isChecked():
            self.change_subject()
        tmp = "FROM - {}     SUBJECT - {}\n\n{}".format(var.inbox_data['from'][row],
                var.inbox_data['subject'][row], var.inbox_data['body'][row])
        GUI.textBrowser_show_email.setText(tmp)

    def email_delete(self):
        try:
            row, column = self.get_index_of_button(GUI.tableWidget_inbox)
            button_delete = QtWidgets.QPushButton('')
            button_delete.setStyleSheet(var.button_style)
            button_delete.clicked.connect(self.email_delete)
            button_delete.setIcon(QtGui.QIcon(var.deleted_icon))
            GUI.tableWidget_inbox.setCellWidget(row, 3, button_delete)
            Thread(target=self.delete, daemon=True, args=[row]).start()
        except:
            pass

    def delete(self, row):
        result = confirm(text='Are you sure?', title='Delete Confirmation Window', buttons=['OK', 'Cancel'])
        if result == 'OK':
            imap.delete_email(row)
            alert(text='Deleted Successfully', title='Alert', button='OK')
        else:
            print("denined")

    def date_update(self):
        var.date = GUI.dateEdit_imap_since.date().toString("M/d/yyyy")

    def get_index_of_button(self, table):
        button = QtWidgets.qApp.focusWidget()
        # or button = self.sender()
        index = table.indexAt(button.pos())
        if index.isValid():
            # print(index.row(), index.column())
            return index.row(), index.column()



if __name__ == '__main__':
    print("ran from here")
else:
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    try:
        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)

        p = resource_path('icons/icon.ico')
        mainWindow.setWindowIcon(QtGui.QIcon(p))
    except Exception as e:
        print(e)

    mainWindow.setWindowFlags(mainWindow.windowFlags(
    ) | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowSystemMenuHint)
    global GUI
    GUI = MyGui(mainWindow)
    # mainWindow.showMaximized()
    mainWindow.show()

    import var
    import imap
    import smtp
    myMC = myMainClass()

    app.exec_()
    print("Exit")
    sys.exit()
