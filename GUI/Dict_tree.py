from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from dict_column_editor_viewer import create_dict_column
import gui_main_interface
import dict_column_editor_viewer

class DictTree(QtWidgets.QTreeWidget):
    def __init__(self, list_of_dict_pref, config, validator, tables_in_receiver, columns_names_source, window_pref, parent=None):
        super().__init__(parent)
        self.window_pref = window_pref
        self.columns_names_source = columns_names_source
        self.tables_in_receiver = tables_in_receiver
        self.validator=validator
        self.setColumnCount(2)
        self.config = config
        self.list_of_dict_pref = list_of_dict_pref
        self.headerItem().setText(0, "Property")
        self.headerItem().setText(1, "Value")

        self.context_menu_duplicate_row = QtWidgets.QMenu()
        self.actionDuplicateTableDict = QtWidgets.QAction()
        self.actionDeleteTableDict = QtWidgets.QAction()
        self.actionDuplicateTableDict.setText("Add Table")
        self.actionDeleteTableDict.setText("Delete Table")
        self.context_menu_duplicate_row.addAction(self.actionDuplicateTableDict)
        self.context_menu_duplicate_row.addAction(self.actionDeleteTableDict)

        self.context_menu_duplicate_replace = QtWidgets.QMenu()
        self.actionDuplicateReplace = QtWidgets.QAction()
        self.actionDeleteReplace = QtWidgets.QAction()
        self.actionDuplicateReplace.setText("Duplicate Replace")
        self.actionDeleteReplace.setText("Delete Replace")
        self.context_menu_duplicate_replace.addAction(self.actionDuplicateReplace)
        self.context_menu_duplicate_replace.addAction(self.actionDeleteReplace)

        self.actionDuplicateTableDict.triggered.connect(self.add_table_dict)
        self.actionDeleteTableDict.triggered.connect(self.delete_table_dict)
        self.actionDuplicateReplace.triggered.connect(self.duplicate_replace)
        self.actionDeleteReplace.triggered.connect(self.delete_replace)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        if self.currentItem():
            if self.currentItem().text(0) == 'table':
                self.context_menu_duplicate_row.exec(event.globalPos())

            try:
                if self.currentItem().checkBox_widget_for_replace_check.text() == 'replace':
                    self.context_menu_duplicate_replace.exec(event.globalPos())
            except:
                pass
        else:
            self.context_menu_duplicate_row.exec(event.globalPos())

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
    def add_table_dict(self):
        dict_pref = {
            'dictTableName': f'{self.window_pref.ui.comboBox_dictTableName.currentText()}',
            'indxDbColumn': None,
            'indxColumnDic': None,
            'colType': None,
            'arrOfDictColumns': None,
            'colName': None,
            'colNameDb': None,
            'cropEnd_mode': 'false',
            'addValueEnd_mode': 'false',
            'takeFromBegin_mode': 'false',
            'cropBegin_mode': 'false',
            'addValueBegin_mode': 'false',
            'addValueBoth_mode': 'false',
            'replace_mode': 'false',

        }
        create_dict_column(pref=self.list_of_dict_pref,
                           parent=self,
                           cur_dic_table_pref=dict_pref,
                           config=self.config,
                           validator=self.validator,
                           tables_in_receiver=self.tables_in_receiver,
                           columns_names_source=self.columns_names_source
                           )

    def delete_table_dict(self):
        cur_column = list(
            filter(lambda x: x['dictTableName'].combo_box_dictTableName.currentText() == self.currentItem().combo_box_dictTableName.currentText(),
                   self.list_of_dict_pref)
        )[0]
        self.list_of_dict_pref.remove(cur_column)
        self.takeTopLevelItem(self.indexFromItem(self.currentItem()).row())









