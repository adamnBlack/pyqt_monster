from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
import var
from p_gui import Ui_Dialog
import os, sys

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

    # def prepare_delete_list()