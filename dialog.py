import sign_in as si
import sign_up as su
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from authentication import Ui_MainWindow
import sys
import os
import re
import requests
from subprocess import check_output
from json import loads, dumps
from threading import Thread
import utils
from pyautogui import confirm

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def check(email):
    # pass the regular expression
    # and the string in search() method
    if(re.search(regex,email)):
        return True
    else:
        return False

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


class Sign_up(su.Ui_Dialog):
    def __init__(self, dialog):
        su.Ui_Dialog.__init__(self)
        self.setupUi(dialog)
        set_icon(dialog)
        self.pushButton_sign_up.clicked.connect(self.validate)
        self.label_status.setText("Password must be equal to or more than 8 characters")
        # self.lineEdit_email.setText("")
        # self.lineEdit_password.setText("123456789")
        # self.lineEdit_confirm_password.setText("123456789")

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.setText)

    def setText(self):
        self.label_status.setText(var.sign_up_label)
    def validate(self):
        email = self.lineEdit_email.text().strip()
        password = self.lineEdit_password.text()
        confirm_password = self.lineEdit_confirm_password.text()
        if check(email):
            print(password, confirm_password)
            if (password != "" and password == confirm_password and len(password) >= 8):
                Thread(target=make_sign_up_requests, daemon=True, args=[email, password, "register"]).start()
                self.timer.start()
                # make_sign_up_requests(email, password, "register")
            else:
                if password != confirm_password:
                    self.label_status.setText("Password don't match")
                else:
                    self.label_status.setText("Password must be equal to or more than 8 characters")
        else:
            self.label_status.setText("Enter a valid email address")

class Sign_in(si.Ui_Dialog):
    def __init__(self, dialog):
        si.Ui_Dialog.__init__(self)
        self.setupUi(dialog)
        self.dialog = dialog
        set_icon(self.dialog)
        self.pushButton_sign_in.clicked.connect(self.validate)
        self.lineEdit_email.setText(var.login_email)
        self.lineEdit_password.setText("123456789")

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.setText)

    def validate(self):
        email = var.login_email = self.lineEdit_email.text().strip()
        password = self.lineEdit_password.text()
        if check(email):
            # print(password)
            # make_sign_up_requests(email, password, "login")
            Thread(target=utils.update_config_json, daemon=True).start()
            self.label_status.setText("connecting main server...")
            Thread(target=make_sign_up_requests, daemon=True, args=[email, password, "login"]).start()
            self.timer.start()
    def setText(self):
        if var.sign_in_label == "Success":
            var.signed_in = True
            self.label_status.setText(var.sign_in_label)
            self.dialog.accept()

        else:
            var.signed_in = False
            self.label_status.setText(var.sign_in_label)

def make_sign_up_requests(email, password, endpoint):
    try:
        status = "Internal error"
        machine_uuid = check_output('wmic csproduct get uuid', shell=False).decode().split('\n')[1].strip()
        processor_id = check_output('wmic cpu get ProcessorId', shell=False).decode().split('\n')[1].strip()
        print(machine_uuid, processor_id)

        url = var.api + 'verify/' + endpoint
        myobj = {
            'machine_uuid': machine_uuid,
            'processor_id': processor_id,
            'email': email,
            'password': password
            }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            }

        data = dumps(myobj).encode("utf-8")
        data = loads(data)
        x = requests.post(url, json=data, headers=headers, timeout=10)

        if len(x.text)>50:
            status = "Error at main server"
        else:
            status = x.text
        print(status)
        if endpoint == 'register':
            var.sign_up_label = status
        else:
            var.sign_in_label = status
    except Exception as e:
        print("Error at reading system info : {}".format(e))
        status = "Couldn't connect"
        print(status)
        if endpoint == 'register':
            var.sign_up_label = status
        else:
            var.sign_in_label = status


class MyGui(Ui_MainWindow, QtWidgets.QWidget):
    def __init__(self, mainWindow):
        Ui_MainWindow.__init__(self)
        QtWidgets.QWidget.__init__(self)
        self.setupUi(mainWindow)

class Communicate(QObject):

    path_picker = pyqtSignal(str, str, int)


class myMainClass():
    def __init__(self):
        GUI.pushButton_sign_in.clicked.connect(self.sign_in)
        GUI.pushButton_sign_up.clicked.connect(self.sign_up)

        self.c = Communicate()
        self.c.path_picker.connect(self.path)
        Thread(target=self.check_update, daemon=True).start()

    def sign_in(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Sign_in(dialog)
        if dialog.exec_():
            app.closeAllWindows()

    def sign_up(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Sign_up(dialog)
        dialog.exec_()

    def check_update(self):
        try:
            url = var.api + "verify/version/{}".format(var.version)
            response = requests.post(url, timeout=10)
            data = response.json()
            if data['update_needed'] == True:
                result = confirm(text='New Version Available!!!\nDo you want to download?',
                            title='Confirmation Window', buttons=['OK', 'Cancel'])
                if result=="OK":
                    # print(data['name'], data['link'], data['size'])
                    self.c.path_picker.emit(data['name'], data['link'], data['size'])
                else:
                    print("Download rejected")
        except Exception as e:
            print("error at check_update: {}".format(e))

    def path(self, name, link, size):
        from progressbar import Download
        print(name, link, size)
        path = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        if path:
            print(path)
            dialog = QtWidgets.QDialog()
            dialog.ui = Download(dialog, name, link, size, path)
            dialog.exec_()
        else:
            print("Download cancelled")

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
    pass
else:
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    set_icon(mainWindow)

    mainWindow.setWindowFlags(mainWindow.windowFlags(
    ) | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowSystemMenuHint)
    GUI = MyGui(mainWindow)
    # mainWindow.showMaximized()
    mainWindow.show()
    import var
    Thread(target=var.load_db, daemon=True, args=("dialog",)).start()
    myMC = myMainClass()

    app.exec_()
    print("Exit")
    if var.signed_in == True:
        import main