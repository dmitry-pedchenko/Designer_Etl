from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from dict_column_editor_viewer import create_dict_column
import gui_main_interface
import dict_column_editor_viewer
from alarm_window import show_alarm_window

class DictTree(QtWidgets.QTreeWidget):
    def __init__(self, list_of_dict_pref, config, validator, tables_in_receiver, columns_names_source, window_pref=None, parent=None):
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

        self.dict_pref = {
            'dictTableName': None,
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
        self.actionDuplicateReplace.setText("Add Replace")
        self.actionDeleteReplace.setText("Delete Replace")
        self.context_menu_duplicate_replace.addAction(self.actionDuplicateReplace)
        self.context_menu_duplicate_replace.addAction(self.actionDeleteReplace)

        self.context_menu_duplicate_column = QtWidgets.QMenu()
        self.actionDuplicateColumn = QtWidgets.QAction()
        self.actionDeleteColumn = QtWidgets.QAction()
        self.actionDuplicateColumn.setText("Add Column")
        self.actionDeleteColumn.setText("Delete Column")
        self.context_menu_duplicate_column.addAction(self.actionDuplicateColumn)
        self.context_menu_duplicate_column.addAction(self.actionDeleteColumn)

        self.actionDuplicateTableDict.triggered.connect(self.add_table_dict)
        self.actionDeleteTableDict.triggered.connect(self.delete_table_dict)
        self.actionDuplicateReplace.triggered.connect(self.duplicate_replace)
        self.actionDeleteReplace.triggered.connect(self.delete_replace)
        self.actionDuplicateColumn.triggered.connect(self.add_column)
        self.actionDeleteColumn.triggered.connect(self.delete_column)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        if self.currentItem():
            try:
                if self.currentItem().text(0) == 'table':
                    self.context_menu_duplicate_row.exec(event.globalPos())
            except:
                pass

            try:
                if self.currentItem().label.text() == 'colName':
                    self.context_menu_duplicate_column.exec(event.globalPos())
            except:
                pass

            try:
                if self.currentItem().checkBox_widget_for_replace_check.text() == 'replace':
                    self.context_menu_duplicate_replace.exec(event.globalPos())
            except:
                pass
        else:
            self.context_menu_duplicate_row.exec(event.globalPos())

    def delete_column(self):
        cur_table = list(
            filter(lambda x: x[
                                 'dictTableName'].combo_box_dictTableName.currentText() == self.currentItem().parent().combo_box_dictTableName.currentText(),
                   self.list_of_dict_pref)
        )[0]['columns']

        if len(cur_table) == 1:
            show_alarm_window(self,"You can't delete last element !!!")
            return

        cur_line = list(
            filter(lambda x: x['colNameRow'].combo_box.currentText() == self.currentItem().combo_box.currentText(),
                    cur_table))[0]

        cur_table.remove(cur_line)

        self.currentItem().parent().takeChild(self.indexFromItem(self.currentItem()).row())



    def add_column(self):
        dict_to_add = {}

        cur_table = list(
            filter(lambda x: x[
                                 'dictTableName'].combo_box_dictTableName.currentText() == self.currentItem().parent().combo_box_dictTableName.currentText(),
                   self.list_of_dict_pref)
        )[0]['columns']

        new_colName = dict_column_editor_viewer.ColumnNameRow(
            column_property=self.dict_pref,
            parent=self.currentItem().parent(),
            tree_widget=self,
            columns_names_source=self.columns_names_source,
            after_widget=self.currentItem(),
        )
        self.addTopLevelItem(new_colName)

        colNameDbRow = dict_column_editor_viewer.ColumnNameDbRow(
            column_property=self.dict_pref,
            parent=new_colName,
            tree_widget=self,
            columns_in_receiver=self.validator.queryForColumns())

        colTypeRow = dict_column_editor_viewer.ColTypeRow(
            cur_dic_table_pref=self.dict_pref,
            parent=new_colName,
            tree_widget=self)

        cropEndRow = dict_column_editor_viewer.CropEndRow(
            column_property=self.dict_pref,
            parent=self,
            parent_widget=new_colName)

        addValueEndRow = dict_column_editor_viewer.AddValueEndRow(
            column_property=self.dict_pref,
            parent=self,
            parent_widget=new_colName )

        takeFromBeginRow = dict_column_editor_viewer.TakeFromBeginRow(
            column_property=self.dict_pref,
            parent=self,
            parent_widget=new_colName)

        cropBeginRow = dict_column_editor_viewer.CropBeginRow(
            column_property=self.dict_pref,
            parent=self,
            parent_widget=new_colName)

        addValueBeginRow = dict_column_editor_viewer.CropBeginRow(
            column_property=self.dict_pref,
            parent=self,
            parent_widget=new_colName)

        addValueBothRow = dict_column_editor_viewer.AddValueBothRow(
            column_property=self.dict_pref,
            parent=self,
            parent_widget=new_colName)

        replace_box = dict_column_editor_viewer.ReplaceRow(
            row=None,
            column_property=self.dict_pref,
            parent=self,
            parent_widget=new_colName,
            after_widget=addValueBothRow,
            table_item=None
        )

        dict_to_add['replace_box'] = []
        dict_to_add['replace_box'].append(replace_box)
        dict_to_add['colNameRow'] = new_colName
        dict_to_add['colNameDbRow'] = colNameDbRow
        dict_to_add['colTypeRow'] = colTypeRow
        dict_to_add['cropEndRow'] = cropEndRow
        dict_to_add['addValueEndRow'] = addValueEndRow
        dict_to_add['takeFromBeginRow'] = takeFromBeginRow
        dict_to_add['cropBeginRow'] = cropBeginRow
        dict_to_add['addValueBeginRow'] = addValueBeginRow
        dict_to_add['addValueBothRow'] = addValueBothRow

        cur_table.append(dict_to_add)

    def duplicate_replace(self):
        replace = dict_column_editor_viewer.ReplaceRow(
            column_property=self.currentItem().column_property,
            parent=self,
            parent_widget=self.currentItem().parent(),
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
        create_dict_column(pref=self.list_of_dict_pref,
                           parent=self,
                           cur_dic_table_pref=self.dict_pref,
                           config=self.config,
                           validator=self.validator,
                           tables_in_receiver=self.tables_in_receiver,
                           columns_names_source=self.columns_names_source
                           )

    def delete_table_dict(self):
        if len(self.list_of_dict_pref) > 1:
            cur_column = list(
                filter(lambda x: x['dictTableName'].combo_box_dictTableName.currentText() == self.currentItem().combo_box_dictTableName.currentText(),
                       self.list_of_dict_pref)
            )[0]
        else:
            show_alarm_window(self,"You can't delete last element !!!")
            return
        self.list_of_dict_pref.remove(cur_column)
        self.takeTopLevelItem(self.indexFromItem(self.currentItem()).row())









