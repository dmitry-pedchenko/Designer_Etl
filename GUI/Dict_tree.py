from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from dict_column_editor_viewer import create_dict_column
import gui_main_interface
import dict_column_editor_viewer

class DictTree(QtWidgets.QTreeWidget):
    def __init__(self, list_of_dict_pref, parent=None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.list_of_dict_pref = list_of_dict_pref
        self.headerItem().setText(0, "Property")
        self.headerItem().setText(1, "Value")

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
        self.actionDuplicateReplace.setText("Duplicate Replace")
        self.actionDeleteReplace.setText("Delete Replace")
        self.context_menu_duplicate_replace.addAction(self.actionDuplicateReplace)
        self.context_menu_duplicate_replace.addAction(self.actionDeleteReplace)

        self.actionDuplicateColumn.triggered.connect(self.add_column)
        self.actionDeleteColumn.triggered.connect(self.delete_column)
        self.actionDuplicateReplace.triggered.connect(self.duplicate_replace)
        self.actionDeleteReplace.triggered.connect(self.delete_replace)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        if self.currentItem().text(0) == 'table':
            self.context_menu_duplicate_row.exec(event.globalPos())

        try:
            if self.currentItem().checkBox_widget_for_replace_check.text() == 'replace':
                self.context_menu_duplicate_replace.exec(event.globalPos())
        except:
            pass

    def duplicate_replace(self):
        replace = dict_column_editor_viewer.ReplaceRow(
            self.currentItem().column_property,
            self,
            self.currentItem().parent(),
            after_widget=self.currentItem(),
            table_item=self.currentItem().parent().parent()

        )

        self.addTopLevelItem(replace)
        cur_table = list(
            filter(lambda x: x['dictTableName'].combo_box_dictTableName.currentText() == self.currentItem().table_item.combo_box_dictTableName.currentText(),
                    self.list_of_dict_pref)
        )[0]['columns']

        list(
        filter(lambda x: x['colNameRow'].combo_box.currentText() == self.currentItem().parent().combo_box.currentText(),
               cur_table)
        )[0]['replace_box'].append(replace)


    def delete_replace(self):
        cur_column = list(
            filter(lambda x: x['dictTableName'].combo_box_dictTableName.currentText() ==
                              self.currentItem().table_item.combo_box_dictTableName.currentText(),
                   self.list_of_dict_pref)
        )[0]['columns']

        element_in_list = list(
            filter(lambda x: x['colNameRow'].combo_box.currentText() == self.currentItem().parent().combo_box.currentText(),
                    cur_column)
        )[0]['replace_box']
        element_in_list.remove(self.currentItem())
        self.currentItem().parent().takeChild(
            self.indexFromItem(self.currentItem()).row())
    def add_column(self):
        create_dict_column(self.list_of_dict_pref,
                           parent=self,
                           cur_column_pref=self.currentItem().cur_column_pref)

    def delete_column(self):
        cur_column = list(
            filter(lambda x: x['dictTableName'].combo_box_dictTableName.currentText() == self.currentItem().combo_box_dictTableName.currentText(),
                   self.list_of_dict_pref)
        )[0]
        self.list_of_dict_pref.remove(cur_column)
        self.takeTopLevelItem(self.indexFromItem(self.currentItem()).row())









