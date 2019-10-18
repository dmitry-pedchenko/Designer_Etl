from PyQt5 import QtCore, QtWidgets
import sys

class Receiver_tree(QtWidgets.QTreeWidget):
    def __init__(self):
        super().__init__()
        self.headerItem().setText(0, "Target rows")



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Receiver_tree()
    w.show()
    sys.exit(app.exec())
