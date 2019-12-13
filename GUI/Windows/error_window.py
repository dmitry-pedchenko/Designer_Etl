from PyQt5 import QtWidgets


def show_error_window(parent, message, error=""):
    QtWidgets.QMessageBox.critical(parent,
                                     'Error',
                                     f"{message} {error}",
                                     QtWidgets.QMessageBox.Ok,
                                     )