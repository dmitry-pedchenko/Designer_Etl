from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import source_column_editor_viewer


class Source_tree(QtWidgets.QTreeWidget):
    def __init__(self):
        super().__init__()
        self.headerItem().setText(0, "Source rows")

        self.context_menu_duplicate_row = QtWidgets.QMenu()
        self.actionDuplicateColumn = QtWidgets.QAction()
        self.actionDeleteColumn = QtWidgets.QAction()
        self.actionDuplicateColumn.setText("Add Column")
        self.actionDeleteColumn.setText("Delete Column")
        self.context_menu_duplicate_row.addAction(self.actionDuplicateColumn)
        self.context_menu_duplicate_row.addAction(self.actionDeleteColumn)

        self.context_menu_duplicate_replace = QtWidgets.QMenu()
        self.actionDuplicateReplace = QtWidgets.QAction()
        self.actionDeleteReplace = QtWidgets.QAction()
        self.actionDuplicateReplace.setText("Add Replace")
        self.actionDeleteReplace.setText("Delete Replace")
        self.context_menu_duplicate_replace.addAction(self.actionDuplicateReplace)
        self.context_menu_duplicate_replace.addAction(self.actionDeleteReplace)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        try:
            if self.currentItem().text(0) == 'colName':
                self.context_menu_duplicate_row.exec(event.globalPos())
                return

            if self.currentItem().checkBox_widget_for_replace_check.text() == 'replace':
                self.context_menu_duplicate_replace.exec(event.globalPos())
                return
        except:
            pass



