import os
import re
import sys
import threading
import webbrowser
import requests
from threading import Thread
from time import sleep
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from pyautogui import alert, confirm
import traceback

from gui import Ui_MainWindow

print("App started....")
quit_application = False


class MyGui(Ui_MainWindow, QtWidgets.QWidget):
    def __init__(self, main_window):
        Ui_MainWindow.__init__(self)
        QtWidgets.QWidget.__init__(self)

        self.setupUi(main_window)


class myMainClass:
    def __init__(self):
        global mainWindow, quit_application, GUI

        self.compose_font_size = 13

        GUI.tabWidget.setCurrentIndex(0)

        # GUI.tableView_database.setContextMenuPolicy(Qt.CustomContextMenu)
        # GUI.tableView_database.customContextMenuRequested.connect(self.showContextMenu)

        GUI.model = TableModel(var.group_a)
        GUI.tableView_database.setModel(GUI.model)
        GUI.tableView_database.show()
        GUI.tableView_database.resizeColumnsToContents()
        delegate = InLineEditDelegate()
        GUI.tableView_database.setItemDelegate(delegate)

        # all types of initialization
        self.logger = var.logging
        self.logger.getLogger("requests").setLevel(var.logging.WARNING)

        # self.font = QtGui.QFont()
        # self.font.setFamily("Calibri")
        # self.font.setBold(True)
        # self.font.setPointSize(11)
        # self.categories = ("Inbox->Primary", "Inbox->Promotions", "Inbox->Social",
        #                 "[Gmail]/Spam")
        # d_categories = ("Primary", "Promotions", "Social", "Spam")
        # GUI.comboBox_email_category.addItems(d_categories)

        self.sub_exp = 0
        self.try_failed = 0

        GUI.lineEdit_email_tracking_analytics_account.setText(
            str(var.tracking['analytics_account']))
        GUI.lineEdit_email_tracking_campaign_name.setText(
            str(var.tracking['campaign_name']))
        GUI.lineEdit_webhook_link.setText(str(var.webhook_link))
        GUI.lineEdit_target_blacklist.setText(",".join(var.target_blacklist))
        GUI.lineEdit_inbox_blacklist.setText(",".join(var.inbox_blacklist))
        GUI.lineEdit_subject.setText(var.compose_email_subject)

        GUI.lineEdit_num_per_address.setText(str(var.num_emails_per_address))
        GUI.lineEdit_delay_between_emails.setText(
            str(var.delay_between_emails))
        GUI.label_version.setText("VERSION: {}".format(var.version))

        self.time_interval_sub_check = 3600
        subscription_thread = Thread(target=self.check_for_subscription, daemon=True).start()

        self.table_timer = QtCore.QTimer()
        self.table_timer.setInterval(10)
        self.table_timer.timeout.connect(self.add_to_table)

        self.command_timer = QtCore.QTimer()
        self.command_timer.setInterval(10)
        self.command_timer.timeout.connect(self.run_command)
        self.command_timer.start()

        date = QtCore.QDate.fromString(var.date, "M/d/yyyy")
        GUI.dateEdit_imap_since.setDate(date)
        # GUI.dateEdit_imap_since.setMaximumDate(QtCore.QDate.currentDate().addDays(-1))

        GUI.dateEdit_imap_since.dateChanged.connect(self.date_update)

        GUI.pushButton_download_email.clicked.connect(self.downloading_email)

        GUI.pushButton_send.clicked.connect(self.send)

        GUI.lineEdit_subject.setText(var.compose_email_subject)
        GUI.textBrowser_compose.setPlainText(var.compose_email_body)

        # set the state of checkboxes
        GUI.checkBox_check_for_blocks.setChecked(var.check_for_blocks)
        GUI.checkBox_responses_webhook.setChecked(var.responses_webhook_enabled)
        GUI.checkBox_responses_webhook.stateChanged.connect(self.update_responses_webhook_enabled)
        GUI.radioButton_html.clicked.connect(self.compose_change)
        GUI.radioButton_plain_text.clicked.connect(self.compose_change)
        GUI.checkBox_compose_preview.clicked.connect(self.compose_preview)
        GUI.lineEdit_subject.textChanged.connect(self.compose_subject_update)

        GUI.pushButton_attachments.clicked.connect(self.openFileNamesDialog)
        GUI.pushButton_attachments_clear.clicked.connect(self.clear_files)

        GUI.pushButton_proxy_provider.clicked.connect(self.proxy_provider)
        GUI.radioButton_reply.clicked.connect(self.change_subject)
        GUI.pushButton_load_db.clicked.connect(self.load_db)
        GUI.pushButton_delete.clicked.connect(self.batch_delete)
        GUI.pushButton_forward.clicked.connect(self.forward)
        GUI.pushButton_test.clicked.connect(self.test_send)
        GUI.textBrowser_show_email.anchorClicked.connect(
            QtGui.QDesktopServices.openUrl)
        GUI.textBrowser_compose.textChanged.connect(self.compose_update)

        GUI.pushButton_config_update.clicked.connect(self.configuration_save)

        GUI.lineEdit_number_of_threads.setText(str(var.limit_of_thread))
        GUI.lineEdit_number_of_threads.textChanged.connect(
            self.update_limit_of_thread)

        GUI.radioButton_db_groupa.clicked.connect(self.update_db_table)
        GUI.radioButton_db_groupb.clicked.connect(self.update_db_table)
        GUI.radioButton_db_target.clicked.connect(self.update_db_table)

        GUI.pushButton_add_row.clicked.connect(self.insert_row)
        GUI.pushButton_remove_row.clicked.connect(self.remove_row)
        Thread(target=database.startup_load_db,
               daemon=True, args=("dialog",)).start()

        GUI.comboBox_date_sort.currentTextChanged.connect(self.date_sort)
        GUI.checkBox_check_for_blocks.stateChanged.connect(
            self.change_check_for_blocks_state)
        GUI.lineEdit_email_tracking_analytics_account.textChanged.connect(
            self.update_email_tracking_link)
        GUI.lineEdit_email_tracking_campaign_name.textChanged.connect(
            self.update_email_tracking_link)

        GUI.pushButton_configuration_save.clicked.connect(
            self.configuration_save)
        GUI.checkBox_email_tracking.stateChanged.connect(
            self.email_tracking_state_update)
        GUI.checkBox_enable_webhook.stateChanged.connect(self.enable_webhook)
        GUI.checkBox_remove_email_from_target.stateChanged.connect(
            self.remove_email_from_target)

        GUI.lineEdit_webhook_link.textChanged.connect(self.update_webhook_link)

        GUI.pushButton_compose_zoomIn.clicked.connect(
            lambda: self.compose_zoomInOut("zoomIn"))
        GUI.pushButton_compose_zoomOut.clicked.connect(
            lambda: self.compose_zoomInOut("zoomOut"))

        GUI.pushButton_compose_send_cancel.clicked.connect(
            self.compose_send_cancel)

        GUI.checkBox_database_group_a.stateChanged.connect(
            self.update_db_file_upload_config)
        GUI.checkBox_database_group_b.stateChanged.connect(
            self.update_db_file_upload_config)
        GUI.checkBox_database_target.stateChanged.connect(
            self.update_db_file_upload_config)

        GUI.checkBox_add_custom_hostname.stateChanged.connect(
            self.update_checkbox_status)

        GUI.pushButton_fire_inbox_webhook.clicked.connect(
            self.start_inbox_stream_thread)

        GUI.lineEdit_target_blacklist.textChanged.connect(
            self.change_target_blacklist)

        GUI.lineEdit_inbox_blacklist.textChanged.connect(
            self.change_inbox_blacklist
        )

        GUI.pushButton_clear_cached_targets.clicked.connect(
            lambda: threading.Thread(target=self.clear_cached_targets, daemon=True, args=[]).start()
        )

    def compose_subject_update(self, value: str):
        var.compose_email_subject = value

    def clear_cached_targets(self):
        db = database.Database()
        db.clear_cached_targets()
        alert(text="Cached cleared.", title='Alert', button='OK')

    def change_target_blacklist(self):
        target_blacklist = GUI.lineEdit_target_blacklist.text().strip().replace(" ", "")
        if target_blacklist:
            var.target_blacklist = target_blacklist.split(",")
        else:
            var.target_blacklist = list()
        print(var.target_blacklist)

    def change_inbox_blacklist(self):
        inbox_blacklist = GUI.lineEdit_inbox_blacklist.text().strip().replace(" ", "")
        if inbox_blacklist:
            var.inbox_blacklist = inbox_blacklist.split(",")
        else:
            var.inbox_blacklist = list()
        print(var.inbox_blacklist)

    def update_responses_webhook_enabled(self):
        var.responses_webhook_enabled = GUI.checkBox_responses_webhook.isChecked()

    def update_checkbox_status(self):
        var.add_custom_hostname = GUI.checkBox_add_custom_hostname.isChecked()

    def update_db_file_upload_config(self):
        var.db_file_loading_config['group_a'] = \
            GUI.checkBox_database_group_a.isChecked()

        var.db_file_loading_config['group_b'] = \
            GUI.checkBox_database_group_b.isChecked()

        var.db_file_loading_config['target'] = \
            GUI.checkBox_database_target.isChecked()

    def showContextMenu(self, pos):
        print("pos " + str(pos))
        index = GUI.tableView_database.indexAt(pos)
        menu = QtWidgets.QMenu()
        menu.addAction("Copy")
        menu.exec_(GUI.tableView_database.viewport().mapToGlobal(pos))

    def remove_email_from_target(self, temp):
        var.remove_email_from_target = GUI.checkBox_remove_email_from_target.isChecked()

    def update_webhook_link(self, text):
        var.webhook_link = str(text)

    def start_inbox_stream_thread(self):
        GUI.tabWidget.setCurrentIndex(0)
        Thread(target=start_inbox_stream, daemon=True).start()

    def enable_webhook(self):
        var.enable_webhook_status = GUI.checkBox_enable_webhook.isChecked()

    def configuration_save(self):
        Thread(target=update_config_json, daemon=True).start()

    def update_email_tracking_link(self):
        var.tracking['analytics_account'] = str(
            GUI.lineEdit_email_tracking_analytics_account.text()).strip()
        pattern = re.compile("[^a-zA-Z0-9_ ]+")
        if not bool(pattern.search(str(GUI.lineEdit_email_tracking_campaign_name.text()).strip())):
            var.tracking['campaign_name'] = str(
                GUI.lineEdit_email_tracking_campaign_name.text()).strip()
        else:
            GUI.lineEdit_email_tracking_campaign_name.setText(
                str(var.tracking['campaign_name']))

    def email_tracking_state_update(self):
        var.email_tracking_state = GUI.checkBox_email_tracking.isChecked()

    def change_check_for_blocks_state(self):
        var.check_for_blocks = GUI.checkBox_check_for_blocks.isChecked()

    def run_command(self):
        try:
            if not var.command_q.empty():
                command = var.command_q.get()
                eval(command)
        except Exception as e:
            print("Error at run_command : {}".format(e))
            self.logger.error("Error at run_command - {}".format(e))

    def insert_row(self):
        GUI.model.insertRows()

    def remove_row(self):
        rows = GUI.tableView_database.selectedIndexes()
        rows = list(set([item.row() for item in rows]))
        if len(rows) == 1:
            GUI.model.removeRows(rows[0])
        elif len(rows) > 1:
            ids = GUI.model._data[GUI.model._data.index.isin(
                rows)].iloc[:, 0].to_list()
            Thread(target=database.db_remove_rows,
                   daemon=True, args=(ids,)).start()
            var.command_q.put(f"GUI.model._data.drop({rows}, inplace=True)")
            var.command_q.put(
                "GUI.model._data.reset_index(drop=True, inplace=True)")
            var.command_q.put("self.update_db_table()")
        else:
            print("Select something")

    def update_db_table(self):
        GUI.model.layoutAboutToBeChanged.emit()
        if GUI.radioButton_db_groupa.isChecked():
            GUI.model._data = var.group_a
        elif GUI.radioButton_db_groupb.isChecked():
            GUI.model._data = var.group_b
        else:
            GUI.model._data = var.target
        GUI.model.layoutChanged.emit()

    def update_limit_of_thread(self):
        try:
            var.limit_of_thread = int(GUI.lineEdit_number_of_threads.text())
        except Exception as e:
            GUI.lineEdit_number_of_threads.setText(str(var.limit_of_thread))
            alert(text="Must be number", title='Alert', button='OK')

    def check_for_subscription(self):
        global quit_application
        while True:
            try:
                url = var.api + \
                      "verify/check_for_subscription/{}".format(var.login_email)
                response = requests.post(url, timeout=10)
                print(response.text)
                data = response.json()

                if response.status_code == 200:
                    if data['status'] == 2:
                        self.try_failed = 0
                        print(data['end_date'])
                        date = str(data['end_date'])

                        quit_application = True
                        var.command_q.put("mainWindow.close()")

                        alert(text="Subscription Expired at {}.\nSoftware will exit soon.".format(date),
                              title='Alert', button='OK')

                    elif data['status'] == 3:
                        self.try_failed = 0
                        print("sub deactivated")

                        quit_application = True
                        var.command_q.put("mainWindow.close()")

                        alert(text="Subscription deativated.\nSoftware will exit soon.",
                              title='Alert', button='OK')

                    elif data['status'] == 1:
                        self.try_failed = 0
                        print(data['days_left'])
                        GUI.label_email_status.setText(
                            "Subscription ends after {} days.".format(data['days_left']))

                    else:
                        self.try_failed = 0

                        quit_application = True
                        var.command_q.put("mainWindow.close()")

                        alert(text="Account not found",
                              title='Alert', button='OK')

                else:
                    quit_application = True
                    var.command_q.put("mainWindow.close()")

                    alert(text="Error on server.\nContact Admin.",
                          title='Alert', button='OK')

            except Exception as e:
                self.try_failed += 1
                print("error at check_for_subcription: {}".format(traceback.format_exc()))

                GUI.label_email_status.setText(
                    "Check your internet connection.")

                if self.try_failed > 3:
                    quit_application = True
                    var.command_q.put("mainWindow.close()")

                    alert(text="Check your internet connection.",
                          title='Alert', button='OK')

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
            temp_df = var.inbox_data.copy()
            temp_df = temp_df.loc[temp_df['checkbox_status'] == 1]

            if temp_df.shape[0] > 0 or GUI.checkBox_delete_all.isChecked() == True:
                result = confirm(
                    text='Are you sure?', title='Confirmation Window', buttons=['OK', 'Cancel'])
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

                    option = str(GUI.comboBox_date_sort.currentText())
                    Thread(target=self.date_sort, daemon=True,
                           args=(option,)).start()

                    # var.inbox_data = pd.DataFrame()
                    # var.row_pos = 0
                    # GUI.tableWidget_inbox.setRowCount(0)
                    # self.table_timer.start()

                else:
                    print("Cancelled")
            else:
                alert(text="You have to make selection first!!!",
                      title="Alert", button="OK")

        except Exception as e:
            print("Error at batch_delete : {}".format(e))
            self.logger.error("Error at batch_delete - {}".format(e))

    def load_db(self):
        result = confirm(text='Are you sure?',
                         title='Confirmation Window', buttons=['OK', 'Cancel'])
        if result == 'OK':
            Thread(target=database.load_db, daemon=True).start()
        else:
            print('cancelled')

    def change_subject(self):
        try:
            subject = var.email_in_view['subject']
            subject = subject if (
                    "RE: " in subject or "Re: " in subject) else "RE: {}".format(subject)
            GUI.lineEdit_subject.setText(subject)
        except Exception as e:
            print("Error while setting subject : {}".format(e))

    def proxy_provider(self):
        webbrowser.open_new(var.proxy_provider)

    def clear_files(self):
        var.files = []

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(
            None, "Attach files", "", "All Files (*)", options=options)
        if files:
            var.files = []
            var.files = files
            GUI.comboBox_attachments.clear()
            GUI.comboBox_attachments.addItems(var.files)

    def compose_zoomInOut(self, source):
        if source == "zoomIn":
            GUI.textBrowser_compose.selectAll()
            self.compose_font_size += 1
            GUI.textBrowser_compose.setFontPointSize(self.compose_font_size)
        else:
            if self.compose_font_size > 2:
                GUI.textBrowser_compose.selectAll()
                self.compose_font_size -= 1
                GUI.textBrowser_compose.setFontPointSize(
                    self.compose_font_size)

    def compose_update(self):
        if not GUI.checkBox_compose_preview.isChecked():
            if GUI.radioButton_html.isChecked():
                var.compose_email_body_html = GUI.textBrowser_compose.toPlainText()
            else:
                var.compose_email_body = GUI.textBrowser_compose.toPlainText()

    def compose_preview(self):
        if GUI.checkBox_compose_preview.isChecked():
            if GUI.radioButton_html.isChecked():
                GUI.textBrowser_compose.setHtml(var.compose_email_body_html)
                GUI.textBrowser_compose.setReadOnly(True)
            else:
                GUI.textBrowser_compose.setReadOnly(False)
                GUI.checkBox_compose_preview.setCheckState(False)
        else:
            if GUI.radioButton_html.isChecked():
                GUI.textBrowser_compose.setPlainText(
                    var.compose_email_body_html)
                GUI.textBrowser_compose.setReadOnly(False)
            else:
                GUI.textBrowser_compose.setPlainText(var.compose_email_body)
                GUI.textBrowser_compose.setReadOnly(False)

    def compose_change(self):
        if GUI.radioButton_html.isChecked():
            GUI.textBrowser_compose.setReadOnly(False)
            GUI.checkBox_compose_preview.setCheckState(False)
            GUI.textBrowser_compose.setPlainText(var.compose_email_body_html)
            var.body_type = "Html"
        else:
            GUI.textBrowser_compose.setReadOnly(False)
            GUI.checkBox_compose_preview.setCheckState(False)
            GUI.textBrowser_compose.setPlainText(var.compose_email_body)
            var.body_type = "Normal"

    def send_button_visibility(self, on=None):
        if on:
            GUI.pushButton_send.setEnabled(True)
            GUI.pushButton_compose_send_cancel.setEnabled(False)
        else:
            GUI.pushButton_send.setEnabled(False)
            GUI.pushButton_compose_send_cancel.setEnabled(True)

    def compose_config_visibility(self, on=None):
        if on:
            GUI.lineEdit_number_of_threads.setEnabled(True)
            GUI.lineEdit_num_per_address.setEnabled(True)
            GUI.radioButton_plain_text.setEnabled(True)
            GUI.radioButton_html.setEnabled(True)
            GUI.checkBox_email_tracking.setEnabled(True)
            GUI.checkBox_enable_webhook.setEnabled(True)
            GUI.checkBox_remove_email_from_target.setEnabled(True)
            GUI.checkBox_check_for_blocks.setEnabled(True)
            GUI.pushButton_attachments.setEnabled(True)
            GUI.pushButton_attachments_clear.setEnabled(True)
            GUI.lineEdit_webhook_link.setEnabled(True)
            GUI.lineEdit_email_tracking_campaign_name.setEnabled(True)
            GUI.lineEdit_email_tracking_analytics_account.setEnabled(True)
            GUI.lineEdit_delay_between_emails.setEnabled(True)
            GUI.tab_database.setEnabled(True)
            GUI.checkBox_add_custom_hostname.setEnabled(True)
        else:
            GUI.lineEdit_number_of_threads.setEnabled(False)
            GUI.lineEdit_num_per_address.setEnabled(False)
            GUI.radioButton_plain_text.setEnabled(False)
            GUI.radioButton_html.setEnabled(False)
            GUI.checkBox_email_tracking.setEnabled(False)
            GUI.checkBox_enable_webhook.setEnabled(False)
            GUI.checkBox_remove_email_from_target.setEnabled(False)
            GUI.checkBox_check_for_blocks.setEnabled(False)
            GUI.pushButton_attachments.setEnabled(False)
            GUI.pushButton_attachments_clear.setEnabled(False)
            GUI.lineEdit_webhook_link.setEnabled(False)
            GUI.lineEdit_email_tracking_campaign_name.setEnabled(False)
            GUI.lineEdit_email_tracking_analytics_account.setEnabled(False)
            GUI.lineEdit_delay_between_emails.setEnabled(False)
            GUI.tab_database.setEnabled(False)
            GUI.checkBox_add_custom_hostname.setEnabled(False)

    def send(self):
        try:
            var.stop_send_campaign = False
            var.thread_open_campaign = 0
            var.send_campaign_email_count = 0

            self.send_button_visibility(on=False)

            if GUI.radioButton_reply.isChecked():
                result = confirm(
                    text='Are you sure?', title='Confirmation Window', buttons=['OK', 'Cancel'])
                if result == 'OK':
                    self.reply()
                else:
                    self.send_button_visibility(on=True)
                    print('cancelled')

            else:
                result = confirm(
                    text='Are you sure?', title='Confirmation Window', buttons=['OK', 'Cancel'])
                if result == 'OK':
                    print("send_campaign")
                    self.send_campaign()
                else:
                    self.send_button_visibility(on=True)
                    print('cancelled')

        except Exception as e:
            print("Error at main.send : {}".format(e))
            self.logger.error("Error at main.send - {}".format(e))

    def compose_send_cancel(self):
        var.stop_send_campaign = True

    def update_compose_progressbar(self):
        try:
            if not var.send_campaign_run_status:
                if var.stop_send_campaign:
                    GUI.label_compose_status.setText(
                        f"Sending Cancelled : {var.send_campaign_email_count}/{self.total_email_to_be_sent} Accounts Failed : {var.email_failed} Targets Remaining : {len(var.target)}")
                else:
                    GUI.label_compose_status.setText(
                        f"Sending Finished : {var.send_campaign_email_count}/{self.total_email_to_be_sent} Accounts Failed : {var.email_failed} Targets Remaining : {len(var.target)}")

            else:
                value = (var.send_campaign_email_count /
                         self.total_email_to_be_sent) * 100
                GUI.label_compose_status.setText(
                    f"Total Email Sent : {var.send_campaign_email_count}/{self.total_email_to_be_sent}")
                GUI.progressBar_compose.setValue(value)

        except Exception as e:
            print("Error at main.py->update_compose_progressbar : {}".format(e))

    def send_campaign(self):
        try:
            global Campaign

            var.send_campaign_run_status = True
            var.num_emails_per_address = int(
                GUI.lineEdit_num_per_address.text())
            var.delay_between_emails = GUI.lineEdit_delay_between_emails.text()
            delay_start = int(var.delay_between_emails.split("-")[0].strip())
            delay_end = int(var.delay_between_emails.split("-")[1].strip())

            Thread(target=update_config_json, daemon=True).start()

            var.compose_email_subject = GUI.lineEdit_subject.text()

            if GUI.radioButton_campaign_group_a.isChecked():
                print("Group a")
                if len(var.group_a) > 0 and len(var.target) > 0:

                    if len(var.group_a) * var.num_emails_per_address > len(var.target):
                        self.total_email_to_be_sent = len(var.target)
                    else:
                        self.total_email_to_be_sent = len(
                            var.group_a) * var.num_emails_per_address

                    Thread(target=smtp.main, daemon=True, args=[
                        var.group_a.copy(), delay_start, delay_end, "Group A", ]).start()

                else:
                    self.send_button_visibility(on=True)
                    GUI.label_email_status.setText("Database empty")
                    var.send_campaign_run_status = False

            else:
                print("Group b")
                if len(var.group_b) > 0 and len(var.target) > 0:

                    if len(var.group_b) * var.num_emails_per_address > len(var.target):
                        self.total_email_to_be_sent = len(var.target)
                    else:
                        self.total_email_to_be_sent = len(
                            var.group_b) * var.num_emails_per_address

                    Thread(target=smtp.main, daemon=True, args=[
                        var.group_b.copy(), delay_start, delay_end, "Group B", ]).start()

                else:
                    self.send_button_visibility(on=True)
                    GUI.label_email_status.setText("Database empty")
                    var.send_campaign_run_status = False

        except Exception as e:
            print("Error at send_campaign : {}".format(e))
            self.logger.error("Error at send_campaign - {}".format(e))
            alert(text="Error at send_campaign : {}".format(
                e), title='Error', button='OK')
            var.send_campaign_run_status = False

    def reply(self):
        var.email_in_view['subject'] = GUI.lineEdit_subject.text()

        if var.body_type == "Html":
            var.email_in_view['body'] = var.compose_email_body_html
        else:
            var.email_in_view['body'] = var.compose_email_body

        dialog = QtWidgets.QDialog()
        dialog.ui = Reply(dialog)
        dialog.exec_()
        self.send_button_visibility(on=True)

    def downloading_email(self):
        try:
            result = confirm(
                text='Are you sure?', title='Confirmation Window', buttons=['OK', 'Cancel'])
            if result == "OK":
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

                dialog = QtWidgets.QDialog()

                if GUI.radioButton_group_a.isChecked() and len(var.group_a) > 0:
                    print("Group a")
                    var.total_acc = len(var.group_a)
                    var.download_email_status = True
                    Thread(target=update_config_json, daemon=True).start()

                    dialog.ui = Download(dialog, var.group_a)

                elif GUI.radioButton_group_b.isChecked() and len(var.group_b) > 0:
                    print("Group b")
                    var.total_acc = len(var.group_b)
                    var.download_email_status = True
                    Thread(target=update_config_json, daemon=True).start()

                    dialog.ui = Download(dialog, var.group_b)

                else:
                    print("no db")
                    alert(text='No database loaded yet!!!',
                          title='Error', button='OK')

                dialog.exec_()
                var.download_email_status = False
                self.table_timer.start()

            else:
                print("Cancelled")
        except Exception as e:
            var.download_email_status = False
            print("Error at downloading_email : {}".format(e))
            self.logger.error("Error at downloading_email - {}".format(e))

    def email_cancel(self):
        result = confirm(text='Are you sure?',
                         title='Confirmation Window', buttons=['OK', 'Cancel'])
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
                var.inbox_data = var.inbox_data.append(
                    row_data, ignore_index=True)

                GUI.tableWidget_inbox.setRowCount(var.row_pos + 1)

                GUI.tableWidget_inbox.setItem(var.row_pos, 1,
                                              QTableWidgetItem(row_data['from']))
                # GUI.tableWidget_inbox.resizeColumnToContents(1)
                GUI.tableWidget_inbox.setItem(var.row_pos, 2,
                                              QTableWidgetItem(row_data['subject']))

                GUI.tableWidget_inbox.setItem(var.row_pos, 3,
                                              QTableWidgetItem(str(row_data['date'].strftime("%b %d %Y %H:%M:%S"))))
                GUI.tableWidget_inbox.resizeColumnToContents(3)

                button_show_mail = QtWidgets.QPushButton('')
                button_show_mail.setStyleSheet(var.button_style)
                button_show_mail.clicked.connect(self.email_show)
                if row_data['flag'] == 'UNSEEN':
                    button_show_mail.setIcon(QtGui.QIcon(var.mail_unread_icon))
                else:
                    button_show_mail.setIcon(QtGui.QIcon(var.mail_read_icon))
                GUI.tableWidget_inbox.setCellWidget(
                    var.row_pos, 0, button_show_mail)

                checkbox_inbox = QtWidgets.QCheckBox(
                    parent=GUI.tableWidget_inbox)
                checkbox_inbox.setStyleSheet(
                    "text-align: center; margin-left:15%; margin-right:10%;")
                checkbox_inbox.stateChanged.connect(self.clickBox)
                GUI.tableWidget_inbox.setCellWidget(
                    var.row_pos, 4, checkbox_inbox)

                GUI.tableWidget_inbox.resizeColumnToContents(0)
                GUI.tableWidget_inbox.resizeColumnToContents(4)
                var.row_pos += 1
                count += 1
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
            if var.inbox_data['flag'][row] == "UNSEEN":
                Thread(target=imap.set_read_flag,
                       daemon=True, args=[row, ]).start()
                var.inbox_data['flag'][row] = "SEEN"
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
                                                                    var.inbox_data['subject'][row],
                                                                    var.inbox_data['body'][row])

                tmp = prepare_html(tmp)

                GUI.textBrowser_show_email.setHtml(tmp)
        except Exception as e:
            print("Error at email_show : {}".format(e))
            self.logger.error("Error at email_show - {}".format(e))

    def date_update(self):
        var.date = GUI.dateEdit_imap_since.date().toString("M/d/yyyy")

    def date_sort(self, option):
        print(option)

        Thread(target=self.sort_inbox_data,
               daemon=True, args=(option,)).start()

    def sort_inbox_data(self, option):
        var.command_q.put("self.table_timer.stop()")

        var.email_in_view = {}

        var.row_pos = 0
        GUI.tableWidget_inbox.setRowCount(0)

        inbox_data = var.inbox_data.copy()

        var.inbox_data = pd.DataFrame()

        if option == "Latest first":
            inbox_data.sort_values(by="date", inplace=True, ascending=True)
        elif option == "a - z":
            inbox_data.sort_values(by="subject", inplace=True, ascending=False)
        elif option == "z - a":
            inbox_data.sort_values(by="subject", inplace=True, ascending=True)
        else:
            inbox_data.sort_values(by="date", inplace=True, ascending=False)

        inbox_data.reset_index(drop=True, inplace=True)
        inbox_data_dict = inbox_data.to_dict("records")

        for index, item in enumerate(inbox_data_dict):
            var.email_q.put(item.copy())

        if inbox_data.shape[0] > 0:
            var.command_q.put("self.table_timer.start()")

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


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

    def closeEvent(self, event):
        close = QtWidgets.QMessageBox.question(self,
                                               "QUIT",
                                               "Are you sure?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if close == QtWidgets.QMessageBox.Yes or quit_application == True:
            myMC.command_timer.stop()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    print("ran from here")
else:
    global app
    global GUI, mainWindow, myMC
    app = QtWidgets.QApplication(sys.argv)

    mainWindow = MainWindow()
    set_icon(mainWindow)

    mainWindow.setWindowFlags(mainWindow.windowFlags(
    ) | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowSystemMenuHint)

    GUI = MyGui(mainWindow)
    mainWindow.showMaximized()
    # mainWindow.show()

    import var
    import imap
    import smtp
    from utils import update_config_json, prepare_html
    from progressbar import Delete_email
    from download_email import Download
    from campaign_reply import Reply
    from send_dialog import Send
    from table_view import TableModel, InLineEditDelegate
    import database
    from webhook import start_inbox_stream

    myMC = myMainClass()

    app.exec_()
    print("Exit")
    sys.exit()
