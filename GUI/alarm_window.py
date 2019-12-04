from PyQt5 import QtWidgets, QtCore

def show_alarm_window(parent, message, error=""):
    QtWidgets.QMessageBox.information(parent,
                                     'Message',
                                     f"{message} {error}",
                                     QtWidgets.QMessageBox.Close,
                                     QtWidgets.QMessageBox.Close,
                                     )