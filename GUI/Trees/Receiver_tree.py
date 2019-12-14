from PyQt5 import QtWidgets
import sys

class Receiver_tree(QtWidgets.QTreeWidget):
    def __init__(self, adapter):
        super().__init__()
        self.headerItem().setText(0, adapter.take_translate('TargetColumnsConfigEditor', 'Target_rows'))

