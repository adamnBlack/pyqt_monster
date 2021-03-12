import datetime
from pyautogui import alert, password, confirm
import json
from threading import Thread
from time import sleep
import os
import sys
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from gui import Ui_MainWindow
import encodings.idna
import pandas as pd
import webbrowser
import subprocess
import requests

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
        global mainWindow
        self.logger = var.logging
        self.logger.getLogger("requests").setLevel(var.logging.WARNING)
        
        self.font = QtGui.QFont()
        self.font.setFamily("Calibri")
        self.font.setBold(True)
        self.font.setPointSize(11)
        # self.categories = ("Inbox->Primary", "Inbox->Promotions", "Inbox->Social", 
        #                 "[Gmail]/Spam")
        # d_categories = ("Primary", "Promotions", "Social", "Spam")
        # GUI.comboBox_email_category.addItems(d_categories)
        self.sub_exp = 0
        self.try_failed = 0

        GUI.lineEdit_num_per_address.setText(str(var.num_emails_per_address))
        GUI.lineEdit_delay_between_emails.setText(str(var.delay_between_emails))
        GUI.label_version.setText("VERSION: {}".format(var.version))

        self.time_interval_sub_check = 3600
        Thread(target=self.check_for_subcription, daemon=True).start()

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

        # GUI.pushButton_send_cancel.setEnabled(True)
        GUI.pushButton_cancel_email.setEnabled(False)
        GUI.lineEdit_subject.setText(var.compose_email_subject)
        GUI.textBrowser_compose.setText(var.compose_email_body)

        GUI.pushButton_attachments.clicked.connect(self.openFileNamesDialog)
        GUI.pushButton_attachments_clear.clicked.connect(self.clear_files)
        GUI.pushButton_email_scraper.clicked.connect(self.email_scraper)
        GUI.pushButton_gmail_provider.clicked.connect(self.gmail_provider)
        GUI.pushButton_proxy_provider.clicked.connect(self.proxy_provider)
        GUI.radioButton_reply.clicked.connect(self.change_subject)
        GUI.pushButton_load_db.clicked.connect(self.load_db)
        GUI.pushButton_clear_compose.clicked.connect(self.clear_compose)
        GUI.pushButton_delete.clicked.connect(self.batch_delete)
        GUI.pushButton_forward.clicked.connect(self.forward)
        GUI.pushButton_test.clicked.connect(self.test_send)
        GUI.textBrowser_show_email.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
                

    def check_for_subcription(self):
        while True:
            try:
                url = var.api + "verify/check_for_subscription/{}".format(var.login_email)
                response = requests.post(url, timeout=10)
                data = response.json()
                
                if response.status_code == 200:
                    if data['status'] == 2:
                        self.try_failed = 0
                        print(data['end_date'])
                        date = str(data['end_date'])
                        alert(text="Subscription Expired at {}.\nSoftware will exit soon.".format(date), 
                                title='Alert', button='OK')
                        mainWindow.close()
                    
                    elif data['status'] == 3:
                        self.try_failed = 0
                        print("sub deactivated")
                        alert(text="Subscription deativated.\nSoftware will exit soon.", 
                                title='Alert', button='OK')
                        mainWindow.close()
                    
                    elif data['status'] == 1:
                        self.try_failed = 0
                        print(data['days_left'])
                        GUI.label_email_status.setText("Subscription ends after {} days.".format(data['days_left']))
                    
                    else:
                        self.try_failed = 0
                        alert(text="Account not found", title='Alert', button='OK')
                        mainWindow.close()

                else:
                    alert(text="Error on server.\nContact Admin.", title='Alert', button='OK')
            
            except Exception as e:
                self.try_failed+=1
                print("error at check_for_subcription: {}".format(e))
                GUI.label_email_status.setText("Check your internet connection.")
                if self.try_failed>3:
                    alert(text="Check your internet connection.",
                                title='Alert', button='OK')
                    mainWindow.close()
            
            sleep(self.time_interval_sub_check)

    def test_send(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Send(dialog, parent='test')
        dialog.exec_()

    def forward(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Send(dialog, parent='forward')
        dialog.exec_()

    def batch_delete(self):
        try:
            result = confirm(text='Are you sure?', title='Confirmation Window', buttons=['OK', 'Cancel'])
            if result == "OK":
                if GUI.checkBox_delete_all.isChecked():
                    result = confirm(text='You are going to delete all?', 
                            title='Confirmation Window', buttons=['Yes', 'No'])
                    if result == "Yes":
                        var.inbox_data["checkbox_status"] = 1
                var.thread_open = 0
                dialog = QtWidgets.QDialog()
                dialog.ui = Delete_email(dialog)
                dialog.exec_()
                var.inbox_data = pd.DataFrame()
                var.row_pos = 0
                GUI.tableWidget_inbox.setRowCount(0)
                self.table_timer.start()
            else:
                print("Cancelled")
        except Exception as e:
            print("Error at batch_delete : {}".format(e))
            self.logger.error("Error at batch_delete - {}".format(e))

    def clear_compose(self):
        GUI.textBrowser_compose.clear()

    def load_db(self):
        Thread(target=var.load_db, daemon=True).start()

    def change_subject(self):
        try:
            subject = var.email_in_view['subject']
            subject = subject if ("RE: " in subject or "Re: " in subject) else "RE: {}".format(subject)
            GUI.lineEdit_subject.setText(subject)
        except Exception as e:
            print("Error while setting subject : {}".format(e))


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
        # options |= QFileDialog.DontUseNativeDialog
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
            GUI.pushButton_send.setEnabled(False)
            GUI.pushButton_send_cancel.setEnabled(False)
            if GUI.radioButton_reply.isChecked():
                result = confirm(text='Are you sure?', title='Confirmation Window', buttons=['OK', 'Cancel'])
                if result == 'OK':
                    Thread(target= self.reply, daemon=True).start()
                    GUI.label_send_email_status.setText("Sending...")
                    GUI.pushButton_send_cancel.setEnabled(True)
                    self.send_progressbar.start()
                else:
                    print('cancelled')
                    GUI.pushButton_send.setEnabled(True)
            else:
                result = confirm(text='Are you sure?', title='Confirmation Window', buttons=['OK', 'Cancel'])
                if result == 'OK':
                    print("send_campaign")
                    Thread(target= self.send_campaign, daemon=True).start()
                    GUI.label_send_email_status.setText("Sending...")
                    GUI.pushButton_send_cancel.setEnabled(True)
                    self.send_progressbar.start()
                else:
                    print('cancelled')
                    GUI.pushButton_send.setEnabled(True)

        except Exception as e:
            print("Error at main.send : {}".format(e))
            self.logger.error("Error at main.send - {}".format(e))



    def send_campaign(self):
        try:
            var.send_campaign_run_status = True
            var.num_emails_per_address = int(GUI.lineEdit_num_per_address.text())
            var.delay_between_emails = GUI.lineEdit_delay_between_emails.text()
            delay_start = int(var.delay_between_emails.split("-")[0].strip())
            delay_end = int(var.delay_between_emails.split("-")[1].strip())
            Thread(target=update_config_json, daemon=True).start()
            var.compose_email_subject = GUI.lineEdit_subject.text()
            var.compose_email_body = GUI.textBrowser_compose.toPlainText()
            # batch = len(var.target)/var.num_emails_per_address
            var.group_a['flag'] = 0
            var.group_b['flag'] = 0
            var.target['flag'] = 0

            if GUI.radioButton_campaign_group_a.isChecked():
                print("Group a")
                if len(var.group_a)>0 and len(var.target)>0:
                    Thread(target=smtp.main, daemon=True, args=[var.group_a.copy(), delay_start, delay_end]).start()
                else:
                    GUI.label_email_status.setText("Database empty")
                    var.send_campaign_run_status = False
                    GUI.pushButton_send.setEnabled(True)


            else:
                print("Group b")
                if len(var.group_b)>0 and len(var.target)>0:
                    Thread(target=smtp.main, daemon=True, args=[var.group_b.copy(), delay_start, delay_end]).start()
                else:
                    GUI.label_email_status.setText("Database empty")
                    var.send_campaign_run_status = False
                    GUI.pushButton_send.setEnabled(True)


        except Exception as e:
            print("Error at send_campaign : {}".format(e))
            self.logger.error("Error at add_to_table - {}".format(e))
            alert(text="Error at send_campaign : {}".format(e), title='Error', button='OK')
            var.send_campaign_run_status = False
            GUI.pushButton_send.setEnabled(True)

    def progressbar_send(self):
        try:
            if var.send_campaign_run_status == False:
                GUI.pushButton_send.setEnabled(True)
                print("Sending finished. Stopping timer.")
                if var.stop_send_campaign == True:
                    GUI.label_send_email_status.setText("Sending Cancelled")
                else:
                    GUI.label_send_email_status.setText("Sending Finished")
                self.send_progressbar.stop()
            else:
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
        except Exception as e:
            print("Error at progressbar_send : {}".format(e))
            self.logger.error("Error at progressbar_send - {}".format(e))

    def reply(self):
        var.email_in_view['subject'] = GUI.lineEdit_subject.text()
        var.email_in_view['body'] = GUI.textBrowser_compose.toPlainText()
        # print(var.email_in_view)
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

    def downloading_email(self):
        try:
            GUI.pushButton_download_email.setEnabled(False)
            GUI.pushButton_cancel_email.setEnabled(True)
            with var.email_q.mutex:
                var.email_q.queue.clear()
            var.total_email = 0
            var.thread_open = 0
            var.acc_finished = 0
            var.stop_download = False
            self.table_timer.stop()
            var.inbox_data = pd.DataFrame()
            var.row_pos = 0
            GUI.tableWidget_inbox.setRowCount(0)
            # category = GUI.comboBox_email_category.currentText()
            # category = self.categories[GUI.comboBox_email_category.currentIndex()]
            # GUI.tableWidget_inbox.horizontalHeaderItem(0).setFont(self.font)
            # GUI.tableWidget_inbox.horizontalHeaderItem(0).setText(GUI.comboBox_email_category.currentText())
            
            if GUI.radioButton_group_a.isChecked() and len(var.group_a) > 0:
                print("Group a")
                GUI.label_email_status.setText("Downloading...")
                var.total_acc = len(var.group_a)
                Thread(target=imap.main, daemon=True, args=[var.group_a,]).start()
                Thread(target=update_config_json, daemon=True).start()
                self.progressbar.start()
            elif GUI.radioButton_group_b.isChecked() and len(var.group_b) > 0:
                print("Group b")
                GUI.label_email_status.setText("Downloading...")
                var.total_acc = len(var.group_b)
                Thread(target=imap.main, daemon=True, args=[var.group_b,]).start()
                Thread(target=update_config_json, daemon=True).start()
                self.progressbar.start()
            else:
                print("no db")
                alert(text='No database loaded yet!!!', title='Error', button='OK')
                GUI.label_email_status.setText("Load Database!!!!")
                GUI.pushButton_download_email.setEnabled(True)
                GUI.pushButton_cancel_email.setEnabled(False)
        except Exception as e:
            print("Error at downloading_email : {}".format(e))
            self.logger.error("Error at downloading_email - {}".format(e))

    # def start_timer(self):
    #     self.table_timer.start()

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
        try:
            count = 0

            while not var.email_q.empty():
                if count == 2:
                    break
                row_data = var.email_q.get()
                row_data['checkbox_status'] = 0
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

                checkbox_inbox = QtWidgets.QCheckBox(parent=GUI.tableWidget_inbox)
                checkbox_inbox.setStyleSheet("text-align: center; margin-left:15%; margin-right:10%;")
                checkbox_inbox.stateChanged.connect(self.clickBox)
                GUI.tableWidget_inbox.setCellWidget(var.row_pos, 3, checkbox_inbox)
                GUI.tableWidget_inbox.resizeColumnToContents(0)
                # GUI.tableWidget_inbox.resizeColumnToContents(1)
                GUI.tableWidget_inbox.resizeColumnToContents(3)
                var.row_pos+=1
                count+=1
            else:
                self.table_timer.stop()
                GUI.label_email_status.setText("Showing Finished")
                print("finished")
        except Exception as e:
            print("Error at add_to_table : {}".format(e))
            self.logger.error("Error at add_to_table - {}".format(e))

    def clickBox(self, state):
        checkbox = GUI.sender()
        # print(ch.parent())
        index = GUI.tableWidget_inbox.indexAt(checkbox.pos())
        # print(index.row(), index.column(), chechbox.isChecked())
        if index.isValid():
            row = index.row()
            if state == QtCore.Qt.Checked:
                print('Checked')
                var.inbox_data['checkbox_status'][row] = 1
                print(var.inbox_data['subject'][row])
            else:
                print('Unchecked')
                var.inbox_data['checkbox_status'][row] = 0
                print(var.inbox_data['subject'][row])


    def email_show(self):
        try:
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
            var.email_in_view = var.inbox_data.iloc[row].to_dict()
            var.email_in_view['original_body'] = var.inbox_data['body'][row]
            var.email_in_view['original_subject'] = var.inbox_data['subject'][row]
            if GUI.radioButton_reply.isChecked():
                self.change_subject()
            
            GUI.textBrowser_show_email.clear()
            if "</body>" in var.inbox_data['body'][row]:
                GUI.textBrowser_show_email.setHtml(var.inbox_data['body'][row])
            else:
                tmp = "FROM - {} <br>SUBJECT - {}<br><br>{}".format(var.inbox_data['from'][row],
                    var.inbox_data['subject'][row], var.inbox_data['body'][row])
                
                tmp = prepare_html(tmp)

                GUI.textBrowser_show_email.setHtml(tmp)
        except Exception as e:
            print("Error at email_show : {}".format(e))
            self.logger.error("Error at email_show - {}".format(e))
        
    # def email_delete(self):
    #     try:
    #         row, column = self.get_index_of_button(GUI.tableWidget_inbox)
    #         button_delete = QtWidgets.QPushButton('')
    #         button_delete.setStyleSheet(var.button_style)
    #         button_delete.clicked.connect(self.email_delete)
    #         button_delete.setIcon(QtGui.QIcon(var.deleted_icon))
    #         GUI.tableWidget_inbox.setCellWidget(row, 3, button_delete)
    #         Thread(target=self.delete, daemon=True, args=[row]).start()
    #     except:
    #         pass

    # def delete(self, row):
    #     result = confirm(text='Are you sure?', title='Delete Confirmation Window', buttons=['OK', 'Cancel'])
    #     if result == 'OK':
    #         imap.delete_email(row)
    #         alert(text='Deleted Successfully', title='Alert', button='OK')
    #     else:
    #         print("denined")

    def date_update(self):
        var.date = GUI.dateEdit_imap_since.date().toString("M/d/yyyy")

    def get_index_of_button(self, table):
        button = QtWidgets.qApp.focusWidget()
        # or button = self.sender()
        index = table.indexAt(button.pos())
        if index.isValid():
            # print(index.row(), index.column())
            return index.row(), index.column()


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


if __name__ == '__main__':
    print("ran from here")
else:
    global app
    global GUI, mainWindow
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    set_icon(mainWindow)

    mainWindow.setWindowFlags(mainWindow.windowFlags(
    ) | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowSystemMenuHint)
    
    GUI = MyGui(mainWindow)
    mainWindow.showMaximized()
    mainWindow.show()

    import var
    import imap
    import smtp
    from utils import update_config_json, prepare_html
    from progressbar import Delete_email
    from send_dialog import Send
    myMC = myMainClass()

    app.exec_()
    print("Exit")
    sys.exit()
