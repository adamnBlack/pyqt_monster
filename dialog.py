import sign_in as si
import sign_up as su
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from authentication import Ui_MainWindow
import sys
import os
import re
import requests
from subprocess import check_output
from json import loads, dumps
from threading import Thread

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
        self.pushButton_sign_up.clicked.connect(self.validate)
        self.label_status.setText("Password must be equal to or more than 8 characters")
        self.lineEdit_email.setText("sdsf@gfdss.com")
        self.lineEdit_password.setText("123456789")
        self.lineEdit_confirm_password.setText("123456789")

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.setText)

    def setText(self):
        self.label_status.setText(var.sign_up_label)
    def validate(self):
        email = self.lineEdit_email.text()
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
        self.pushButton_sign_in.clicked.connect(self.validate)
        self.lineEdit_email.setText("sdsf@gfdss.com")
        self.lineEdit_password.setText("123456789")

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.setText)

    def validate(self):
        email = self.lineEdit_email.text()
        password = self.lineEdit_password.text()
        if check(email):
            print(password)
            # make_sign_up_requests(email, password, "login")
            self.label_status.setText("connecting main server...")
            Thread(target=make_sign_up_requests, daemon=True, args=[email, password, "login"]).start()
            self.timer.start()
    def setText(self):
        if var.sign_in_label == "Success":
            var.signed_in = True
            self.label_status.setText(var.sign_in_label)
            self.dialog.accept()
            app.closeAllWindows()
        else:
            var.signed_in = False
            self.label_status.setText(var.sign_in_label)

def make_sign_up_requests(email, password, endpoint):
    try:
        status = "Internal error"
        machine_uuid = check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        processor_id = check_output('wmic cpu get ProcessorId').decode().split('\n')[1].strip()
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



class myMainClass():
    def __init__(self):
        GUI.pushButton_sign_in.clicked.connect(self.sign_in)
        GUI.pushButton_sign_up.clicked.connect(self.sign_up)

    def sign_in(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Sign_in(dialog)
        dialog.exec_()


    def sign_up(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Sign_up(dialog)
        dialog.exec_()


if __name__ == '__main__':
    pass
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
    GUI = MyGui(mainWindow)
    # mainWindow.showMaximized()
    mainWindow.show()
    import var
    myMC = myMainClass()

    app.exec_()
    print("Exit")
    if var.signed_in == True:
        import main