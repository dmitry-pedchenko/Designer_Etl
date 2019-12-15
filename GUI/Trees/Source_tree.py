from PyQt5 import QtWidgets, QtGui


class Source_tree(QtWidgets.QTreeWidget):
    def __init__(self, adapter):
        super().__init__()
        self.headerItem().setText(0, f"{adapter.take_translate('SourceColumnsConfigEditor', 'SourceRows')}")

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
            if self.currentItem() is None:
                self.context_menu_duplicate_row.exec(event.globalPos())
                return

            if self.currentItem().objectName == 'colName':
                self.context_menu_duplicate_row.exec(event.globalPos())
                return

            if self.currentItem().objectName == 'replace':
                self.context_menu_duplicate_replace.exec(event.globalPos())
                return
        except:
            pass



