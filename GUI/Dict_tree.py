from PyQt5 import QtWidgets, QtGui, QtCore
import sys


class DictTree(QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.headerItem().setText(0, "Property")
        self.headerItem().setText(1, "Value")






