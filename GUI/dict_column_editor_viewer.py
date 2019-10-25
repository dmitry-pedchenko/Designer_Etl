from PyQt5 import QtWidgets, QtCore, QtGui
import sys

def create_dict_column(pref, parent, cur_column_pref):
    dict_pref = {}
    dict_pref['columns'] = []

    main_row = MainDictTableName(cur_column_pref, parent)
    dict_pref_indxDbColumn = IndxDbColumn(cur_column_pref, parent=main_row, tree_widget=parent)
    dict_pref_indxColumnDic = IndxColumnDic(cur_column_pref, parent=main_row, tree_widget=parent)

    for row in cur_column_pref['arrOfDictColumns']:
        temp_dict = {}
        temp_dict['replace_box'] = []

        colNameRow = ColumnNameRow(row, main_row,parent)
        colNameDbRow = ColumnNameDbRow(row, colNameRow, parent)
        colTypeRow = ColTypeRow(row, colNameRow, tree_widget=parent)
        cropEndRow = CropEndRow(row, parent, colNameRow)
        addValueEndRow = AddValueEndRow(row, parent, colNameRow)
        takeFromBeginRow = TakeFromBeginRow(row, parent, colNameRow)
        cropBeginRow = CropBeginRow(row, parent, colNameRow)
        addValueBeginRow = CropBeginRow(row, parent, colNameRow)
        addValueBothRow = AddValueBothRow(row, parent, colNameRow)

        if row['replace_mode'] == 'true':
            link_to_prior = None
            for count, replace in enumerate(row['replaceValArr']):
                if link_to_prior is not None:
                    replace_box = ReplaceRow(
                        row=replace,
                        column_property=row,
                        parent=parent,
                        parent_widget=colNameRow,
                        after_widget=link_to_prior,
                        table_item=main_row
                    )
                else:
                    replace_box = ReplaceRow(
                        row=replace,
                        column_property=row,
                        parent=parent,
                        parent_widget=colNameRow,
                        after_widget=addValueBothRow,
                        table_item=main_row
                    )
                link_to_prior = replace_box
                parent.addTopLevelItem(replace_box)
                temp_dict['replace_box'].append(replace_box)
        else:
            replace_box = ReplaceRow(
                        row=None,
                        column_property=row,
                        parent=parent,
                        parent_widget=colNameRow,
                        after_widget=addValueBothRow,
                        table_item=main_row
                    )

            parent.addTopLevelItem(replace_box)
            temp_dict['replace_box'].append(replace_box)



        temp_dict['colNameRow'] = colNameRow
        temp_dict['colNameDbRow'] = colNameDbRow
        temp_dict['colTypeRow'] = colTypeRow
        temp_dict['cropEndRow'] = cropEndRow
        temp_dict['addValueEndRow'] = addValueEndRow
        temp_dict['takeFromBeginRow'] = takeFromBeginRow
        temp_dict['cropBeginRow'] = cropBeginRow
        temp_dict['addValueBeginRow'] = addValueBeginRow
        temp_dict['addValueBothRow'] = addValueBothRow

        dict_pref['columns'].append(temp_dict)





    dict_pref['dictTableName'] = main_row
    dict_pref['indxDbColumn'] = dict_pref_indxDbColumn
    dict_pref['indxColumnDic'] = dict_pref_indxColumnDic

    pref.append(dict_pref)


class MainDictTableName(QtWidgets.QTreeWidgetItem):
    def __init__(self, cur_column_pref, parent):
        super().__init__(parent, ['table', ])
        self.cur_column_pref = cur_column_pref
        # test data
        list_combo_box_dictTableName = ['dic_1', 'dic_2']
        #

        self.combo_box_dictTableName = QtWidgets.QComboBox()
        self.combo_box_dictTableName.addItems(list_combo_box_dictTableName)
        self.combo_box_dictTableName.setCurrentIndex(list_combo_box_dictTableName.index(cur_column_pref['dictTableName']))
        parent.setItemWidget(self, 1, self.combo_box_dictTableName)


class IndxDbColumn(QtWidgets.QTreeWidgetItem):
    def __init__(self, cur_column_pref, parent, tree_widget):
        super().__init__(parent, ['indxDbColumn', ])
        # test data
        list_indxDbColumn = ['indx_1', 'indx_2']
        #
        combo_box_indxDbColumn = QtWidgets.QComboBox()
        combo_box_indxDbColumn.addItems(list_indxDbColumn)
        combo_box_indxDbColumn.setCurrentIndex(list_indxDbColumn.index(cur_column_pref['indxDbColumn']))
        tree_widget.setItemWidget(self, 1, combo_box_indxDbColumn)


class ColTypeRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, cur_column_pref, parent, tree_widget):
        super().__init__(parent, ['colType', ])

        list_of_types_dict_to_comboBox = {'String': 'str', 'Float': 'float', 'Integer': 'int', 'Date': 'date'}
        list_of_coltypes_in_comboBox = ['String', 'Float', 'Integer', 'Date']

        self.combo_box_colType = QtWidgets.QComboBox()
        self.combo_box_colType.addItems(list_of_coltypes_in_comboBox)

        tree_widget.setItemWidget(self, 1, self.combo_box_colType)

        self.combo_box_colType.setCurrentIndex(
            list_of_coltypes_in_comboBox.index(
                list(filter(lambda x: list_of_types_dict_to_comboBox[x] == cur_column_pref['colType'],
                            list_of_types_dict_to_comboBox))[0]))


class IndxColumnDic(QtWidgets.QTreeWidgetItem):
    def __init__(self, cur_column_pref, parent, tree_widget):
        super().__init__(parent, ['indxColumnDic', ])
        #
        list_indxColumnDic = ['indx']
        #
        combo_box_indxColumnDic = QtWidgets.QComboBox()
        combo_box_indxColumnDic.addItems(list_indxColumnDic)
        combo_box_indxColumnDic.setCurrentIndex(list_indxColumnDic.index(cur_column_pref['indxColumnDic']))
        tree_widget.setItemWidget(self, 1, combo_box_indxColumnDic)


#
#
class ColumnNameRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property, parent, tree_widget):
        super().__init__(parent, ["colName", column_property['colName']])
        # test data
        list_combo_box_dictTableName = ['dict_1_1', 'dict_1_2', 'dict_1_3','dict_2_1', 'dict_2_2', 'dict_2_3']
        #
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(list_combo_box_dictTableName)
        self.combo_box.setCurrentIndex(list_combo_box_dictTableName.index(column_property['colName']))
        self.column_property = column_property
        tree_widget.setItemWidget(self, 1, self.combo_box)


class ColumnNameDbRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property, parent, tree_widget):
        super().__init__(parent, ["colNameDb", column_property['colNameDb']])
        #
        list_colname_in_db_dict = ['col_1', 'col_2', 'col_3']
        #
        self.combo_box_colnameDb = QtWidgets.QComboBox()
        self.combo_box_colnameDb.addItems(list_colname_in_db_dict)
        self.combo_box_colnameDb.setCurrentIndex(list_colname_in_db_dict.index(column_property['colNameDb']))
        tree_widget.setItemWidget(self, 1, self.combo_box_colnameDb)


class CropEndRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_cropEnd_check = QtWidgets.QCheckBox('cropEnd')

        self.spin_box_cropEnd = QtWidgets.QSpinBox()
        self.spin_box_cropEnd.setRange(0, 255)

        parent.setItemWidget(self, 0, self.checkBox_widget_for_cropEnd_check)
        parent.setItemWidget(self, 1, self.spin_box_cropEnd)

        self.initialize()

        self.checkBox_widget_for_cropEnd_check.stateChanged.connect(self.state_change)

    def state_change(self):
        if self.checkBox_widget_for_cropEnd_check.isChecked():
            self.spin_box_cropEnd.setDisabled(False)
        else:
            self.spin_box_cropEnd.setDisabled(True)

    def initialize(self):
        if self.column_property['cropEnd_mode'] != 'false':
            self.spin_box_cropEnd.setValue(int(self.column_property['cropEnd']))
            self.checkBox_widget_for_cropEnd_check.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBox_widget_for_cropEnd_check.setCheckState(QtCore.Qt.Unchecked)
            self.spin_box_cropEnd.setDisabled(True)


class AddValueEndRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_addValueEnd_check = QtWidgets.QCheckBox('addValueEnd')
        self.line_edit_addValueEnd = QtWidgets.QLineEdit()

        parent.setItemWidget(self, 0, self.checkBox_widget_for_addValueEnd_check)
        parent.setItemWidget(self, 1, self.line_edit_addValueEnd)

        self.initialize()

        self.checkBox_widget_for_addValueEnd_check.stateChanged.connect(self.state_change)

    def initialize(self):
        if self.column_property['addValueEnd_mode'] != 'false':
            self.line_edit_addValueEnd.setText(self.column_property['addValueEnd'])
            self.checkBox_widget_for_addValueEnd_check.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBox_widget_for_addValueEnd_check.setCheckState(QtCore.Qt.Unchecked)
            self.line_edit_addValueEnd.setDisabled(True)

    def state_change(self):
        if self.checkBox_widget_for_addValueEnd_check.isChecked():
            self.line_edit_addValueEnd.setDisabled(False)
        else:
            self.line_edit_addValueEnd.setDisabled(True)


class TakeFromBeginRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_takeFromBegin_check = QtWidgets.QCheckBox('takeFromBegin')

        self.spin_box_takeFromBegin = QtWidgets.QSpinBox()
        self.spin_box_takeFromBegin.setRange(0, 255)

        parent.setItemWidget(self, 0, self.checkBox_widget_for_takeFromBegin_check)
        parent.setItemWidget(self, 1, self.spin_box_takeFromBegin)

        self.initialize()

        self.checkBox_widget_for_takeFromBegin_check.stateChanged.connect(self.state_change)

    def initialize(self):
        if self.column_property['takeFromBegin_mode'] != 'false':
            self.spin_box_takeFromBegin.setValue(int(self.column_property['takeFromBegin']))
            self.checkBox_widget_for_takeFromBegin_check.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBox_widget_for_takeFromBegin_check.setCheckState(QtCore.Qt.Unchecked)
            self.spin_box_takeFromBegin.setDisabled(True)

    def state_change(self):
        if self.checkBox_widget_for_takeFromBegin_check.isChecked():
            self.spin_box_takeFromBegin.setDisabled(False)
        else:
            self.spin_box_takeFromBegin.setDisabled(True)


class CropBeginRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_cropBegin_check = QtWidgets.QCheckBox('cropBegin')
        self.spin_box_cropBegin = QtWidgets.QSpinBox()
        self.spin_box_cropBegin.setRange(0, 255)

        parent.setItemWidget(self, 0, self.checkBox_widget_for_cropBegin_check)
        parent.setItemWidget(self, 1, self.spin_box_cropBegin)

        self.initialize()

        self.checkBox_widget_for_cropBegin_check.stateChanged.connect(self.state_change)

    def initialize(self):
        if self.column_property['cropBegin_mode'] != 'false':
            self.spin_box_cropBegin.setValue(int(self.column_property['cropBegin']))
            self.checkBox_widget_for_cropBegin_check.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBox_widget_for_cropBegin_check.setCheckState(QtCore.Qt.Unchecked)
            self.spin_box_cropBegin.setDisabled(True)

    def state_change(self):
        if self.checkBox_widget_for_cropBegin_check.isChecked():
            self.spin_box_cropBegin.setDisabled(False)
        else:
            self.spin_box_cropBegin.setDisabled(True)


class AddValueBeginRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_addValueBegin_check = QtWidgets.QCheckBox('addValueBegin')

        self.line_edit_addValueBegin = QtWidgets.QLineEdit()

        parent.setItemWidget(self, 0, self.checkBox_widget_for_addValueBegin_check)
        parent.setItemWidget(self, 1, self.line_edit_addValueBegin)

        self.initialize()

        self.checkBox_widget_for_addValueBegin_check.stateChanged.connect(self.state_change)

    def initialize(self):
        if self.column_property['addValueBegin_mode'] != 'false':
            self.line_edit_addValueBegin.setText(self.column_property['addValueBegin'])
            self.checkBox_widget_for_addValueBegin_check.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBox_widget_for_addValueBegin_check.setCheckState(QtCore.Qt.Unchecked)
            self.line_edit_addValueBegin.setDisabled(True)

    def state_change(self):
        if self.checkBox_widget_for_addValueBegin_check.isChecked():
            self.line_edit_addValueBegin.setDisabled(False)
        else:
            self.line_edit_addValueBegin.setDisabled(True)


class AddValueBothRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property

        self.widget_for_add_both_filter = QtWidgets.QWidget()
        hbox_layout_both_filter = QtWidgets.QHBoxLayout()
        self.line_edit_addBegin_Both_filter = QtWidgets.QLineEdit()
        text_begin_for_addBegin_Both_filter = QtWidgets.QLabel('To begin')
        self.line_edit_addEnd_Both_filter = QtWidgets.QLineEdit()
        text_end_for_addBegin_Both_filter = QtWidgets.QLabel('To end')
        hbox_layout_both_filter.addWidget(text_begin_for_addBegin_Both_filter)
        hbox_layout_both_filter.addWidget(self.line_edit_addBegin_Both_filter)
        hbox_layout_both_filter.addWidget(text_end_for_addBegin_Both_filter)
        hbox_layout_both_filter.addWidget(self.line_edit_addEnd_Both_filter)
        self.widget_for_add_both_filter.setLayout(hbox_layout_both_filter)

        self.checkBox_widget_for_addValueBoth_check = QtWidgets.QCheckBox('addValueBoth')

        parent.setItemWidget(self, 0, self.checkBox_widget_for_addValueBoth_check)
        parent.setItemWidget(self, 1, self.widget_for_add_both_filter)

        self.initialize()

        self.checkBox_widget_for_addValueBoth_check.stateChanged.connect(self.state_change)

    def initialize(self):
        if self.column_property['addValueBoth_mode'] != 'false':
            self.line_edit_addBegin_Both_filter.setText(self.column_property['addValueBoth'].split(',')[0])
            self.line_edit_addEnd_Both_filter.setText(self.column_property['addValueBoth'].split(',')[1])
            self.checkBox_widget_for_addValueBoth_check.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBox_widget_for_addValueBoth_check.setCheckState(QtCore.Qt.Unchecked)
            self.line_edit_addBegin_Both_filter.setDisabled(True)
            self.line_edit_addEnd_Both_filter.setDisabled(True)

    def state_change(self):
        if self.checkBox_widget_for_addValueBoth_check.isChecked():
            self.line_edit_addBegin_Both_filter.setDisabled(False)
            self.line_edit_addEnd_Both_filter.setDisabled(False)
        else:
            self.line_edit_addBegin_Both_filter.setDisabled(True)
            self.line_edit_addEnd_Both_filter.setDisabled(True)


class ReplaceRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget, after_widget=None, row: dict=None, table_item=None):
        super().__init__(parent_widget, after_widget)
        self.column_property = column_property
        self.table_item = table_item
        self.row = row
        self.widget_for_replace = QtWidgets.QWidget()
        hbox_layout_replace = QtWidgets.QHBoxLayout()
        self.line_edit_addBegin_Both = QtWidgets.QLineEdit()
        text_begin_for_replace = QtWidgets.QLabel('Initial')
        self.line_edit_addEnd_Both = QtWidgets.QLineEdit()
        text_end_for_replace = QtWidgets.QLabel('Final')
        hbox_layout_replace.addWidget(text_begin_for_replace)
        hbox_layout_replace.addWidget(self.line_edit_addBegin_Both)
        hbox_layout_replace.addWidget(text_end_for_replace)
        hbox_layout_replace.addWidget(self.line_edit_addEnd_Both)
        self.widget_for_replace.setLayout(hbox_layout_replace)

        self.checkBox_widget_for_replace_check = QtWidgets.QCheckBox('replace')

        parent.setItemWidget(self, 0, self.checkBox_widget_for_replace_check)
        parent.setItemWidget(self, 1, self.widget_for_replace)
        self.initialize()
        self.checkBox_widget_for_replace_check.stateChanged.connect(self.state_change)

    def initialize(self):
        if self.row:
            if self.column_property['replace_mode'] != 'false':
                self.line_edit_addBegin_Both.setText(self.row['replaceValue'])
                self.line_edit_addEnd_Both.setText(self.row['replaceToValue'])
                self.checkBox_widget_for_replace_check.setCheckState(QtCore.Qt.Checked)
            else:
                self.checkBox_widget_for_replace_check.setCheckState(QtCore.Qt.Unchecked)
                self.line_edit_addBegin_Both.setDisabled(True)
                self.line_edit_addEnd_Both.setDisabled(True)

    def state_change(self):
        if self.checkBox_widget_for_replace_check.isChecked():
            self.line_edit_addBegin_Both.setDisabled(False)
            self.line_edit_addEnd_Both.setDisabled(False)
        else:
            self.line_edit_addBegin_Both.setDisabled(True)
            self.line_edit_addEnd_Both.setDisabled(True)
