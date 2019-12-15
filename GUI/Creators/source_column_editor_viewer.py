from PyQt5 import QtWidgets, QtCore
import datetime
from GUI.Windows.alarm_window import show_alarm_window


def create_input_column(tree_table: QtWidgets.QTreeWidget,
                        db_colnames: list,
                        column_property: dict,
                        list_of_cols: list,
                        indx=None,
                        source_columnes: list=None,
                        adapter=None
                        ):
    tree_table.setColumnCount(2)
    tree_table.setHeaderLabels([adapter.take_translate('SourceColumnsConfigEditor', 'PropertyNameCOLUMN'),
                                adapter.take_translate('SourceColumnsConfigEditor', 'ValueCOLUMN')])
    dic = {}
    dic['replace_box'] = []

    combo_box_colType = QtWidgets.QComboBox()
    list_of_types_dict_to_comboBox = {'String': 'str', 'Float': 'float', 'Integer': 'int', 'Date': 'date', '---': '---'}
    list_of_coltypes_in_comboBox = ['String', 'Float', 'Integer', 'Date', '---']
    combo_box_colType.addItems(list_of_coltypes_in_comboBox)
    list_of_state_dict_isPk = {'True': 'true', 'False': 'false'}
    combo_box_isPk = QtWidgets.QCheckBox()
    state = list(filter(lambda x: list_of_state_dict_isPk[x] == column_property['isPK'],
                                             list_of_state_dict_isPk))[0]


    combo_box_dbName = QtWidgets.QComboBox()

    for name in db_colnames:
        combo_box_dbName.addItem(name)

    if state == 'True':
        combo_box_isPk.setCheckState(QtCore.Qt.Checked)
    elif state == 'False':
        combo_box_isPk.setCheckState(QtCore.Qt.Unchecked)
    else:
        raise SystemError('Unknown state')


    #
    # create tree widget item
    if column_property['colNameDb']:
        combo_box_dbName.setCurrentIndex(db_colnames.index(column_property['colNameDb']))
    else:
        combo_box_dbName.addItem('---')
        combo_box_dbName.setCurrentText('---')
    if column_property['colType']:
        combo_box_colType.setCurrentIndex(
            list_of_coltypes_in_comboBox.index(
                list(filter(lambda x: list_of_types_dict_to_comboBox[x] == column_property['colType'],
                            list_of_types_dict_to_comboBox))[0]))

    colName_box = ColumnNameRow(
        column_property=column_property,
        arr_of_db_columns=source_columnes,
        tree_widget=tree_table,
        adapter=adapter
    )
    colNameDb_box = QtWidgets.QTreeWidgetItem(colName_box, [adapter.take_translate('SourceColumnsConfigEditor', 'colNameDb'), ])
    colType_box = QtWidgets.QTreeWidgetItem(colName_box, [adapter.take_translate('SourceColumnsConfigEditor', 'colType'), ])
    isPK_box = QtWidgets.QTreeWidgetItem(colName_box, [adapter.take_translate('SourceColumnsConfigEditor', 'isPk'), ])
    cropEnd_box = CropEndRow(column_property, tree_table, parent_widget=colName_box, adapter=adapter)
    addValueEnd_box = AddValueEndRow(column_property, tree_table, parent_widget=colName_box, adapter=adapter)
    takeFromBegin_box = TakeFromBeginRow(column_property, tree_table, parent_widget=colName_box, adapter=adapter)
    cropBegin_box = CropBeginRow(column_property, tree_table, parent_widget=colName_box, adapter=adapter)
    addValueBegin_box = AddValueBeginRow(column_property, tree_table, parent_widget=colName_box, adapter=adapter)
    addValueBoth_box = AddValueBothRow(column_property, tree_table, parent_widget=colName_box, adapter=adapter)

    if column_property['replace_mode'] == 'true':
        link_to_prior = None
        for count, replace in enumerate(column_property['replaceValArr']):
            if link_to_prior is not None:
                replace_box = ReplaceRow(
                    row=replace,
                    column_property=column_property,
                    parent=tree_table,
                    parent_widget=colName_box,
                    after_widget=link_to_prior,
                    adapter=adapter
                )
            else:
                replace_box = ReplaceRow(
                    row=replace,
                    column_property=column_property,
                    parent=tree_table,
                    parent_widget=colName_box,
                    after_widget=addValueBoth_box,
                    adapter=adapter
                )
            link_to_prior = replace_box
            tree_table.addTopLevelItem(replace_box)
            dic['replace_box'].append(replace_box)

    else:
        replace_box = ReplaceRow(
                row=None,
                column_property=column_property,
                parent=tree_table,
                parent_widget=colName_box,
                after_widget=addValueBoth_box,
                adapter=adapter
            )

        tree_table.addTopLevelItem(replace_box)
        dic['replace_box'].append(replace_box)

    filter_box = FilterRow(column_property, tree_table, widget=combo_box_colType, parent_widget=colName_box, coltypes=list_of_coltypes_in_comboBox,adapter=adapter)
    post_filter_box = PostFilterRow(column_property, tree_table, widget=combo_box_colType, parent_widget=colName_box, coltypes=list_of_coltypes_in_comboBox, adapter=adapter)

    if indx is not None:
        tree_table.insertTopLevelItem(indx, colName_box)
    else:
        tree_table.addTopLevelItem(colName_box)

    tree_table.setItemWidget(colNameDb_box, 1, combo_box_dbName)
    tree_table.setItemWidget(colType_box, 1, combo_box_colType)
    tree_table.setItemWidget(isPK_box, 1, combo_box_isPk)



    dic['colName'] = colName_box
    dic['isPK'] = combo_box_isPk
    dic['colType'] = combo_box_colType
    dic['colNameDb'] = combo_box_dbName
    dic['cropEnd_box'] = cropEnd_box
    dic['addValueEnd_box'] = addValueEnd_box
    dic['takeFromBegin_box'] = takeFromBegin_box
    dic['cropBegin_box'] = cropBegin_box
    dic['addValueBegin_box'] = addValueBegin_box
    dic['addValueBoth_box'] = addValueBoth_box

    dic['filter_box'] = filter_box
    dic['post_filter_box'] = post_filter_box

    list_of_cols.append(dic)

    filter_box.checkBox_widget_for_filter_check.stateChanged.emit(0)


class ColumnNameRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property, arr_of_db_columns, tree_widget, adapter):
        super().__init__(tree_widget, [adapter.take_translate('SourceColumnsConfigEditor', 'colName'), ])
        self.combo_box_name = QtWidgets.QComboBox()
        self.tree_widget = tree_widget
        self.combo_box_name.addItems(arr_of_db_columns)
        self.combo_box_name.addItem('---')
        self.objectName = "colName"

        if column_property['colName']:
            self.combo_box_name.setCurrentIndex(arr_of_db_columns.index(column_property['colName']))
        else:
            self.combo_box_name.setCurrentText('---')

        tree_widget.setItemWidget(self, 1, self.combo_box_name)


class CropEndRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget, adapter):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_cropEnd_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'cropEnd'))

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
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget, adapter):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_addValueEnd_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'addValueEnd'))

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
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget, adapter):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_takeFromBegin_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'takeFromBegin'))

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
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget, adapter):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_cropBegin_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'cropBegin'))
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
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget, adapter):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_addValueBegin_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'addValueBegin'))

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
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget, adapter):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property

        self.widget_for_add_both_filter = QtWidgets.QWidget()
        hbox_layout_both_filter = QtWidgets.QHBoxLayout()
        self.line_edit_addBegin_Both_filter = QtWidgets.QLineEdit()
        text_begin_for_addBegin_Both_filter = QtWidgets.QLabel(adapter.take_translate('SourceColumnsConfigEditor', 'To_begin'))
        self.line_edit_addEnd_Both_filter = QtWidgets.QLineEdit()
        text_end_for_addBegin_Both_filter = QtWidgets.QLabel(adapter.take_translate('SourceColumnsConfigEditor', 'To_end'))
        hbox_layout_both_filter.addWidget(text_begin_for_addBegin_Both_filter)
        hbox_layout_both_filter.addWidget(self.line_edit_addBegin_Both_filter)
        hbox_layout_both_filter.addWidget(text_end_for_addBegin_Both_filter)
        hbox_layout_both_filter.addWidget(self.line_edit_addEnd_Both_filter)
        self.widget_for_add_both_filter.setLayout(hbox_layout_both_filter)

        self.checkBox_widget_for_addValueBoth_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'addValueBoth'))

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
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget, after_widget=None, row: dict=None, adapter=None):
        super().__init__(parent_widget, after_widget)
        self.column_property = column_property
        self.row = row
        self.objectName = 'replace'
        self.widget_for_replace = QtWidgets.QWidget()
        hbox_layout_replace = QtWidgets.QHBoxLayout()
        self.line_edit_addBegin_Both = QtWidgets.QLineEdit()
        text_begin_for_replace = QtWidgets.QLabel(adapter.take_translate('SourceColumnsConfigEditor', 'Initial'))
        self.line_edit_addEnd_Both = QtWidgets.QLineEdit()
        text_end_for_replace = QtWidgets.QLabel(adapter.take_translate('SourceColumnsConfigEditor', 'Final'))
        hbox_layout_replace.addWidget(text_begin_for_replace)
        hbox_layout_replace.addWidget(self.line_edit_addBegin_Both)
        hbox_layout_replace.addWidget(text_end_for_replace)
        hbox_layout_replace.addWidget(self.line_edit_addEnd_Both)
        self.widget_for_replace.setLayout(hbox_layout_replace)

        self.checkBox_widget_for_replace_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'replace'))

        parent.setItemWidget(self, 0, self.checkBox_widget_for_replace_check)
        parent.setItemWidget(self, 1, self.widget_for_replace)
        self.initialize()
        self.checkBox_widget_for_replace_check.stateChanged.connect(self.state_change)

    def initialize(self):
        if self.row:
            if self.column_property['replace_mode'] == 'true':
                self.line_edit_addBegin_Both.setText(self.row['replaceValue'])
                self.line_edit_addEnd_Both.setText(self.row['replaceToValue'])
                self.checkBox_widget_for_replace_check.setCheckState(QtCore.Qt.Checked)
            else:
                self.checkBox_widget_for_replace_check.setCheckState(QtCore.Qt.Unchecked)
                self.line_edit_addBegin_Both.setDisabled(True)
                self.line_edit_addEnd_Both.setDisabled(True)
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


class FilterRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget, widget: QtWidgets.QComboBox,
                 coltypes: list, adapter):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.coltypes = coltypes
        self.parent = parent
        self.adapter = adapter
        self.checkBox_widget_for_filter_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'filter'))
        self.checkBox_widget_f_cropEnd_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'f_cropEnd'))
        self.checkBox_widget_f_addValueEnd_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'f_addValueEnd'))
        self.checkBox_widget_f_takeFromBegin_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'f_takeFromBegin'))
        self.checkBox_widget_f_cropBegin_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'f_cropBegin'))
        self.checkBox_widget_f_addValueBegin_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'f_addValueBegin'))
        self.checkBox_widget_f_addValueBoth_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'f_addValueBoth'))

        self.spin_box_f_cropEnd = QtWidgets.QSpinBox()
        self.spin_box_f_cropEnd.setRange(0, 255)

        self.line_edit_f_addValueEnd = QtWidgets.QLineEdit()

        self.spin_box_f_takeFromBegin = QtWidgets.QSpinBox()
        self.spin_box_f_takeFromBegin.setRange(0, 255)

        self.spin_box_f_cropBegin = QtWidgets.QSpinBox()
        self.spin_box_f_cropBegin.setRange(0, 255)

        self.line_edit_f_addValueBegin = QtWidgets.QLineEdit()

        self.widget_for_add_both_filter = QtWidgets.QWidget()
        hbox_layout_both_filter = QtWidgets.QHBoxLayout()
        self.line_edit_addBegin_Both_filter = QtWidgets.QLineEdit()
        text_begin_for_addBegin_Both_filter = QtWidgets.QLabel(adapter.take_translate('SourceColumnsConfigEditor', 'To_begin'))
        self.line_edit_addEnd_Both_filter = QtWidgets.QLineEdit()
        text_end_for_addBegin_Both_filter = QtWidgets.QLabel(adapter.take_translate('SourceColumnsConfigEditor', 'To_end'))
        hbox_layout_both_filter.addWidget(text_begin_for_addBegin_Both_filter)
        hbox_layout_both_filter.addWidget(self.line_edit_addBegin_Both_filter)
        hbox_layout_both_filter.addWidget(text_end_for_addBegin_Both_filter)
        hbox_layout_both_filter.addWidget(self.line_edit_addEnd_Both_filter)
        self.widget_for_add_both_filter.setLayout(hbox_layout_both_filter)

        self.filter_box_sub_f_cropEnd = QtWidgets.QTreeWidgetItem(self, ['', ])
        self.filter_box_sub_f_addValueEnd = QtWidgets.QTreeWidgetItem(self, ['', ])
        self.filter_box_sub_f_takeFromBegin = QtWidgets.QTreeWidgetItem(self, ['', ])
        self.filter_box_sub_f_cropBegin = QtWidgets.QTreeWidgetItem(self, ['', ])
        self.filter_box_sub_f_addValueBegin = QtWidgets.QTreeWidgetItem(self, ['', ])
        self.filter_box_sub_f_addValueBoth = QtWidgets.QTreeWidgetItem(self, ['', ])
        self.filter_box_sub_filter_state = QtWidgets.QTreeWidgetItem(self, [adapter.take_translate('SourceColumnsConfigEditor', 'filter'), ])

        parent.addTopLevelItem(self.filter_box_sub_f_cropEnd)
        parent.addTopLevelItem(self.filter_box_sub_f_addValueEnd)
        parent.addTopLevelItem(self.filter_box_sub_f_takeFromBegin)
        parent.addTopLevelItem(self.filter_box_sub_f_cropBegin)
        parent.addTopLevelItem(self.filter_box_sub_f_addValueBegin)
        parent.addTopLevelItem(self.filter_box_sub_f_addValueBoth)

        parent.setItemWidget(self.filter_box_sub_f_cropEnd, 1, self.spin_box_f_cropEnd)
        parent.setItemWidget(self.filter_box_sub_f_addValueEnd, 1, self.line_edit_f_addValueEnd)
        parent.setItemWidget(self.filter_box_sub_f_takeFromBegin, 1, self.spin_box_f_takeFromBegin)
        parent.setItemWidget(self.filter_box_sub_f_cropBegin, 1, self.spin_box_f_cropBegin)
        parent.setItemWidget(self.filter_box_sub_f_addValueBegin, 1, self.line_edit_f_addValueBegin)
        parent.setItemWidget(self.filter_box_sub_f_addValueBoth, 1, self.widget_for_add_both_filter)

        parent.setItemWidget(self, 0, self.checkBox_widget_for_filter_check)
        parent.setItemWidget(self.filter_box_sub_f_cropEnd, 0, self.checkBox_widget_f_cropEnd_check)
        parent.setItemWidget(self.filter_box_sub_f_addValueEnd, 0, self.checkBox_widget_f_addValueEnd_check)
        parent.setItemWidget(self.filter_box_sub_f_takeFromBegin, 0, self.checkBox_widget_f_takeFromBegin_check)
        parent.setItemWidget(self.filter_box_sub_f_cropBegin, 0, self.checkBox_widget_f_cropBegin_check)
        parent.setItemWidget(self.filter_box_sub_f_addValueBegin, 0, self.checkBox_widget_f_addValueBegin_check)
        parent.setItemWidget(self.filter_box_sub_f_addValueBoth, 0, self.checkBox_widget_f_addValueBoth_check)

        self.initialize()
        self.checkBox_widget_for_filter_check.stateChanged.connect(self.state_change)

        self.checkBox_widget_f_cropEnd_check.stateChanged.connect(self.state_change_cropEnd)
        self.checkBox_widget_f_addValueEnd_check.stateChanged.connect(self.state_change_addValueEnd)
        self.checkBox_widget_f_takeFromBegin_check.stateChanged.connect(self.state_change_takeFromBegin)
        self.checkBox_widget_f_cropBegin_check.stateChanged.connect(self.state_change_cropBegin)
        self.checkBox_widget_f_addValueBegin_check.stateChanged.connect(self.state_change_addValueBegin)
        self.checkBox_widget_f_addValueBoth_check.stateChanged.connect(self.state_change_addValueBoth)

        widget.currentIndexChanged.connect(self.set_data_type_widget)


    def initialize(self):
        if self.column_property['filter_mode'] == 'true':
            self.checkBox_widget_for_filter_check.setCheckState(QtCore.Qt.Checked)

            if self.column_property['filter_dict_edit']['cropEnd_mode'] == 'true':
                self.spin_box_f_cropEnd.setValue(int(self.column_property['filter_dict_edit']['cropEnd']))
                self.checkBox_widget_f_cropEnd_check.setCheckState(QtCore.Qt.Checked)
            if self.column_property['filter_dict_edit']['cropEnd_mode'] == 'false':
                self.checkBox_widget_f_cropEnd_check.setCheckState(QtCore.Qt.Unchecked)
                self.spin_box_f_cropEnd.setDisabled(True)

            if self.column_property['filter_dict_edit']['addValueEnd_mode'] == 'true':
                self.line_edit_f_addValueEnd.setText(self.column_property['filter_dict_edit']['addValueEnd'])
                self.checkBox_widget_f_addValueEnd_check.setCheckState(QtCore.Qt.Checked)
            if self.column_property['filter_dict_edit']['addValueEnd_mode'] == 'false':
                self.checkBox_widget_f_addValueEnd_check.setCheckState(QtCore.Qt.Unchecked)
                self.line_edit_f_addValueEnd.setDisabled(True)

            if self.column_property['filter_dict_edit']['takeFromBegin_mode'] == 'true':
                self.spin_box_f_takeFromBegin.setValue(int(self.column_property['filter_dict_edit']['takeFromBegin']))
                self.checkBox_widget_f_takeFromBegin_check.setCheckState(QtCore.Qt.Checked)
            if self.column_property['filter_dict_edit']['takeFromBegin_mode'] == 'false':
                self.checkBox_widget_f_takeFromBegin_check.setCheckState(QtCore.Qt.Unchecked)
                self.spin_box_f_takeFromBegin.setDisabled(True)

            if self.column_property['filter_dict_edit']['cropBegin_mode'] == 'true':
                self.spin_box_f_cropBegin.setValue(int(self.column_property['filter_dict_edit']['cropBegin']))
                self.checkBox_widget_f_cropBegin_check.setCheckState(QtCore.Qt.Checked)
            if self.column_property['filter_dict_edit']['cropBegin_mode'] == 'false':
                self.checkBox_widget_f_cropBegin_check.setCheckState(QtCore.Qt.Unchecked)
                self.spin_box_f_cropBegin.setDisabled(True)

            if self.column_property['filter_dict_edit']['addValueBegin_mode'] == 'true':
                self.line_edit_f_addValueBegin.setText(self.column_property['filter_dict_edit']['addValueBegin'])
                self.checkBox_widget_f_addValueBegin_check.setCheckState(QtCore.Qt.Checked)
            if self.column_property['filter_dict_edit']['addValueBegin_mode'] == 'false':
                self.checkBox_widget_f_addValueBegin_check.setCheckState(QtCore.Qt.Unchecked)
                self.line_edit_f_addValueBegin.setDisabled(True)
            if self.column_property['filter_dict_edit']['addValueBoth_mode'] == 'true':
                self.line_edit_addBegin_Both_filter.setText(self.column_property['filter_dict_edit']['addValueBoth'].split(',')[0])
                self.line_edit_addEnd_Both_filter.setText(self.column_property['filter_dict_edit']['addValueBoth'].split(',')[1])
                self.checkBox_widget_f_addValueBoth_check.setCheckState(QtCore.Qt.Checked)
            if self.column_property['filter_dict_edit']['addValueBoth_mode'] == 'false':
                self.checkBox_widget_f_addValueBoth_check.setCheckState(QtCore.Qt.Unchecked)
                self.line_edit_addBegin_Both_filter.setDisabled(True)
                self.line_edit_addEnd_Both_filter.setDisabled(True)
                self.widget_for_add_both_filter.setDisabled(True)

            if self.column_property['colType'] == 'str':
                self.line_edit_addEnd_filter = QtWidgets.QLineEdit()
                self.line_edit_addEnd_filter.setText(self.column_property['filterArr'][0]['filterValue'])
            if self.column_property['colType'] == 'int':
                self.line_edit_addEnd_filter = QtWidgets.QSpinBox()
                self.line_edit_addEnd_filter.setRange(-10000, 10000)
                self.line_edit_addEnd_filter.setValue(int(self.column_property['filterArr'][0]['filterValue']))
            if self.column_property['colType'] == 'float':
                self.line_edit_addEnd_filter = QtWidgets.QDoubleSpinBox()
                self.line_edit_addEnd_filter.setRange(-10000, 10000)
                self.line_edit_addEnd_filter.setValue(float(self.column_property['filterArr'][0]['filterValue']))
            if self.column_property['colType'] == 'date':
                self.line_edit_addEnd_filter = QtWidgets.QDateEdit()
                self.line_edit_addEnd_filter.setDisplayFormat("yyyy.MM.dd")
                self.line_edit_addEnd_filter.setCalendarPopup(True)
                try:
                    self.line_edit_addEnd_filter.setDate(
                    datetime.datetime.strptime(self.column_property['filterArr'][0]['filterValue'], "%Y.%m.%d"))
                except Exception as e:
                    show_alarm_window(self, f"Wrong date format in config file. <{e}> !!!")
                    return

            if self.column_property['colType'] != 'str':
                self.combo_box_filter_condition = QtWidgets.QComboBox()
                self.list_of_types_equals_for_filter = ['!=', '=', '>', '<', '<=', '>=', '---']
                self.combo_box_filter_condition.addItems(self.list_of_types_equals_for_filter)
            if self.column_property['colType'] == 'str':
                self.combo_box_filter_condition = QtWidgets.QComboBox()
                self.list_of_types_equals_for_filter = ['!=', '=', '---']
                self.combo_box_filter_condition.addItems(self.list_of_types_equals_for_filter)

            self.widget_for_filter = QtWidgets.QWidget()
            hbox_layout_filter = QtWidgets.QHBoxLayout()
            text_begin_for_addBegin_filter = QtWidgets.QLabel(self.adapter.take_translate('SourceColumnsConfigEditor', 'Condition'))
            text_end_for_addBegin_filter = QtWidgets.QLabel(self.adapter.take_translate('SourceColumnsConfigEditor', 'ValueCOLUMN'))
            hbox_layout_filter.addWidget(text_begin_for_addBegin_filter)
            hbox_layout_filter.addWidget(self.combo_box_filter_condition)
            hbox_layout_filter.addWidget(text_end_for_addBegin_filter)
            hbox_layout_filter.addWidget(self.line_edit_addEnd_filter)
            self.widget_for_filter.setLayout(hbox_layout_filter)

            self.parent.setItemWidget(self.filter_box_sub_filter_state, 1, self.widget_for_filter)
            if self.column_property['filterArr'][0]['filterMode']:
                try:
                    self.combo_box_filter_condition.setCurrentIndex(
                    self.list_of_types_equals_for_filter.index(self.column_property['filterArr'][0]['filterMode']))
                except Exception as e:
                    show_alarm_window(self, f"Wrong filter mode. <{e}> !!!")
                    self.combo_box_filter_condition.setCurrentText('---')
                    return
            else:
                self.combo_box_filter_condition.setCurrentText('---')


        else:
            self.checkBox_widget_for_filter_check.setCheckState(QtCore.Qt.Unchecked)

            if self.column_property['colType'] == 'str':
                self.line_edit_addEnd_filter = QtWidgets.QLineEdit()
            if self.column_property['colType'] == 'int':
                self.line_edit_addEnd_filter = QtWidgets.QSpinBox()
                self.line_edit_addEnd_filter.setRange(-10000, 10000)
            if self.column_property['colType'] == 'float':
                self.line_edit_addEnd_filter = QtWidgets.QDoubleSpinBox()
                self.line_edit_addEnd_filter.setRange(-10000, 10000)
            if self.column_property['colType'] == 'date':
                self.line_edit_addEnd_filter = QtWidgets.QDateEdit()
                self.line_edit_addEnd_filter.setDisplayFormat("yyyy.MM.dd")
                self.line_edit_addEnd_filter.setCalendarPopup(True)
            if self.column_property['colType'] == '---':
                self.line_edit_addEnd_filter = QtWidgets.QLineEdit()
                self.line_edit_addEnd_filter.setText('---')

            if self.column_property['colType'] != 'str':
                self.combo_box_filter_condition = QtWidgets.QComboBox()
                self.list_of_types_equals_for_filter = ['!=', '=', '>', '<', '<=', '>=', '---']
                self.combo_box_filter_condition.addItems(self.list_of_types_equals_for_filter)
            if self.column_property['colType'] == 'str':
                self.combo_box_filter_condition = QtWidgets.QComboBox()
                self.list_of_types_equals_for_filter = ['!=', '=', '---']
                self.combo_box_filter_condition.addItems(self.list_of_types_equals_for_filter)
            if self.column_property['colType'] == '---':
                self.combo_box_filter_condition = QtWidgets.QComboBox()
                self.list_of_types_equals_for_filter = ['---']
                self.combo_box_filter_condition.addItems(self.list_of_types_equals_for_filter)


            self.widget_for_filter = QtWidgets.QWidget()
            hbox_layout_filter = QtWidgets.QHBoxLayout()
            text_begin_for_addBegin_filter = QtWidgets.QLabel(self.adapter.take_translate('SourceColumnsConfigEditor', 'Condition'))
            text_end_for_addBegin_filter = QtWidgets.QLabel(self.adapter.take_translate('SourceColumnsConfigEditor', 'ValueCOLUMN'))
            hbox_layout_filter.addWidget(text_begin_for_addBegin_filter)
            hbox_layout_filter.addWidget(self.combo_box_filter_condition)
            hbox_layout_filter.addWidget(text_end_for_addBegin_filter)
            hbox_layout_filter.addWidget(self.line_edit_addEnd_filter)
            self.widget_for_filter.setLayout(hbox_layout_filter)

            self.parent.setItemWidget(self.filter_box_sub_filter_state, 1, self.widget_for_filter)
            #
            self.combo_box_filter_condition.setDisabled(True)
            self.line_edit_addEnd_filter.setDisabled(True)
            self.spin_box_f_cropEnd.setDisabled(True)
            self.line_edit_f_addValueEnd.setDisabled(True)
            self.spin_box_f_takeFromBegin.setDisabled(True)
            self.spin_box_f_cropBegin.setDisabled(True)
            self.line_edit_f_addValueBegin.setDisabled(True)
            self.line_edit_addEnd_Both_filter.setDisabled(True)
            self.line_edit_addBegin_Both_filter.setDisabled(True)
            self.widget_for_add_both_filter.setDisabled(True)

    def state_change_cropEnd(self):
        if self.checkBox_widget_f_cropEnd_check.isChecked():
            self.spin_box_f_cropEnd.setDisabled(False)
        else:
            self.spin_box_f_cropEnd.setDisabled(True)

    def state_change_addValueEnd(self):
        if self.checkBox_widget_f_addValueEnd_check.isChecked():
            self.line_edit_f_addValueEnd.setDisabled(False)
        else:
            self.line_edit_f_addValueEnd.setDisabled(True)

    def state_change_takeFromBegin(self):
        if self.checkBox_widget_f_takeFromBegin_check.isChecked():
            self.spin_box_f_takeFromBegin.setDisabled(False)
        else:
            self.spin_box_f_takeFromBegin.setDisabled(True)

    def state_change_cropBegin(self):
        if self.checkBox_widget_f_cropBegin_check.isChecked():
            self.spin_box_f_cropBegin.setDisabled(False)
        else:
            self.spin_box_f_cropBegin.setDisabled(True)

    def state_change_addValueBegin(self):
        if self.checkBox_widget_f_addValueBegin_check.isChecked():
            self.line_edit_f_addValueBegin.setDisabled(False)
        else:
            self.line_edit_f_addValueBegin.setDisabled(True)

    def state_change_addValueBoth(self):
        if self.checkBox_widget_f_addValueBoth_check.isChecked():
            self.line_edit_addBegin_Both_filter.setDisabled(False)
            self.line_edit_addEnd_Both_filter.setDisabled(False)
            self.widget_for_add_both_filter.setDisabled(False)
        else:
            self.line_edit_addBegin_Both_filter.setDisabled(True)
            self.line_edit_addEnd_Both_filter.setDisabled(True)
            self.widget_for_add_both_filter.setDisabled(True)

    def state_change(self):
        if self.checkBox_widget_for_filter_check.isChecked():
            self.filter_box_sub_f_cropEnd.setHidden(False)
            self.filter_box_sub_f_addValueEnd.setHidden(False)
            self.filter_box_sub_f_takeFromBegin.setHidden(False)
            self.filter_box_sub_f_cropBegin.setHidden(False)
            self.filter_box_sub_f_addValueBegin.setHidden(False)
            self.filter_box_sub_f_addValueBoth.setHidden(False)
            self.filter_box_sub_filter_state.setHidden(False)
            self.combo_box_filter_condition.setDisabled(False)
            self.line_edit_addEnd_filter.setDisabled(False)
        else:
            self.filter_box_sub_f_cropEnd.setHidden(True)
            self.filter_box_sub_f_addValueEnd.setHidden(True)
            self.filter_box_sub_f_takeFromBegin.setHidden(True)
            self.filter_box_sub_f_cropBegin.setHidden(True)
            self.filter_box_sub_f_addValueBegin.setHidden(True)
            self.filter_box_sub_f_addValueBoth.setHidden(True)
            self.filter_box_sub_filter_state.setHidden(True)

    def set_data_type_widget(self, index):

        if self.coltypes[index] == 'String':
            self.line_edit_addEnd_filter = QtWidgets.QLineEdit()
        if self.coltypes[index] == 'Integer':
            self.line_edit_addEnd_filter = QtWidgets.QSpinBox()
            self.line_edit_addEnd_filter.setRange(-10000, 10000)
        if self.coltypes[index] == 'Float':
            self.line_edit_addEnd_filter = QtWidgets.QDoubleSpinBox()
            self.line_edit_addEnd_filter.setRange(-10000, 10000)
        if self.coltypes[index] == 'Date':
            self.line_edit_addEnd_filter = QtWidgets.QDateEdit()
            self.line_edit_addEnd_filter.setDisplayFormat("yyyy.MM.dd")
            self.line_edit_addEnd_filter.setCalendarPopup(True)
        if self.coltypes[index] == '---':
            self.line_edit_addEnd_filter = QtWidgets.QLineEdit()
            self.line_edit_addEnd_filter.setText('---')

        if self.coltypes[index] != 'String':
            self.combo_box_filter_condition = QtWidgets.QComboBox()
            self.list_of_types_equals_for_filter = ['!=', '=', '>', '<', '<=', '>=']
            self.combo_box_filter_condition.addItems(self.list_of_types_equals_for_filter)
        if self.coltypes[index] == 'String':
            self.combo_box_filter_condition = QtWidgets.QComboBox()
            self.list_of_types_equals_for_filter = ['!=', '=']
            self.combo_box_filter_condition.addItems(self.list_of_types_equals_for_filter)
        if self.coltypes[index] == '---':
            self.combo_box_filter_condition = QtWidgets.QComboBox()
            list_of_types_equals_for_filter = ['---']
            self.combo_box_filter_condition.addItems(list_of_types_equals_for_filter)

        #
        #
        self.widget_for_filter = QtWidgets.QWidget()
        hbox_layout_filter = QtWidgets.QHBoxLayout()
        text_begin_for_addBegin_filter = QtWidgets.QLabel(self.adapter.take_translate('SourceColumnsConfigEditor', 'Condition'))
        text_end_for_addBegin_filter = QtWidgets.QLabel(self.adapter.take_translate('SourceColumnsConfigEditor', 'ValueCOLUMN'))
        hbox_layout_filter.addWidget(text_begin_for_addBegin_filter)
        hbox_layout_filter.addWidget(self.combo_box_filter_condition)
        hbox_layout_filter.addWidget(text_end_for_addBegin_filter)
        hbox_layout_filter.addWidget(self.line_edit_addEnd_filter)
        self.widget_for_filter.setLayout(hbox_layout_filter)

        self.parent.setItemWidget(self.filter_box_sub_filter_state, 1, self.widget_for_filter)


class PostFilterRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget, widget: QtWidgets.QComboBox, coltypes: list, adapter):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.adapter = adapter
        self.parent = parent
        self.coltypes = coltypes
        if self.column_property['colType'] != 'str':
            self.combo_box_post_filter_condition = QtWidgets.QComboBox()
            list_of_post_filter_conditions = ['!=', '=', '>', '<', '<=', '>=']
            self.combo_box_post_filter_condition.addItems(list_of_post_filter_conditions)
        if self.column_property['colType'] == 'str':
            self.combo_box_post_filter_condition = QtWidgets.QComboBox()
            list_of_post_filter_conditions = ['!=', '=']
            self.combo_box_post_filter_condition.addItems(list_of_post_filter_conditions)
        if self.column_property['colType'] == '---':
            self.combo_box_post_filter_condition = QtWidgets.QComboBox()
            list_of_post_filter_conditions = ['---']
            self.combo_box_post_filter_condition.addItems(list_of_post_filter_conditions)

        if self.column_property['colType'] == 'str':
            self.line_edit_post_filter = QtWidgets.QLineEdit()
        if self.column_property['colType'] == 'int':
            self.line_edit_post_filter = QtWidgets.QSpinBox()
            self.line_edit_post_filter.setRange(-10000, 10000)
        if self.column_property['colType'] == 'float':
            self.line_edit_post_filter = QtWidgets.QDoubleSpinBox()
            self.line_edit_post_filter.setRange(-10000, 10000)
        if self.column_property['colType'] == 'date':
            self.line_edit_post_filter = QtWidgets.QDateEdit()
            self.line_edit_post_filter.setDisplayFormat("yyyy.MM.dd")
            self.line_edit_post_filter.setCalendarPopup(True)
        if self.column_property['colType'] == '---':
            self.line_edit_post_filter = QtWidgets.QLineEdit()
            self.line_edit_post_filter.setText('---')

        self.widget_for_post_filter = QtWidgets.QWidget()
        hbox_layout_post_filter = QtWidgets.QHBoxLayout()
        text_begin_for_addBegin_post_filter = QtWidgets.QLabel(adapter.take_translate('SourceColumnsConfigEditor', 'Condition'))
        text_end_for_addBegin_post_filter = QtWidgets.QLabel(adapter.take_translate('SourceColumnsConfigEditor', 'ValueCOLUMN'))
        hbox_layout_post_filter.addWidget(text_begin_for_addBegin_post_filter)
        hbox_layout_post_filter.addWidget(self.combo_box_post_filter_condition)
        hbox_layout_post_filter.addWidget(text_end_for_addBegin_post_filter)
        hbox_layout_post_filter.addWidget(self.line_edit_post_filter)
        self.widget_for_post_filter.setLayout(hbox_layout_post_filter)

        self.checkBox_widget_for_post_filter_check = QtWidgets.QCheckBox(adapter.take_translate('SourceColumnsConfigEditor', 'post_filter'))

        self.initialize()

        self.parent.setItemWidget(self, 0, self.checkBox_widget_for_post_filter_check)
        self.parent.setItemWidget(self, 1, self.widget_for_post_filter)

        self.checkBox_widget_for_post_filter_check.stateChanged.connect(self.state_change)
        widget.currentIndexChanged.connect(self.set_data_type_widget)

    def state_change(self):
        if self.checkBox_widget_for_post_filter_check.isChecked():
            self.combo_box_post_filter_condition.setDisabled(False)
            self.line_edit_post_filter.setDisabled(False)
            self.widget_for_post_filter.setDisabled(False)
        else:
            self.combo_box_post_filter_condition.setDisabled(True)
            self.line_edit_post_filter.setDisabled(True)
            self.widget_for_post_filter.setDisabled(True)

    def initialize(self):
        if self.column_property['post_filter_mode'] == 'true':
            self.checkBox_widget_for_post_filter_check.setCheckState(QtCore.Qt.Checked)

            if self.column_property['colType'] == 'str':
                self.line_edit_post_filter.setText(self.column_property['postfilterArr'][0]['filterValue'])
            if self.column_property['colType'] == 'int':
                self.line_edit_post_filter.setValue(int(self.column_property['postfilterArr'][0]['filterValue']))
            if self.column_property['colType'] == 'float':
                self.line_edit_post_filter.setValue(float(self.column_property['postfilterArr'][0]['filterValue']))
            if self.column_property['colType'] == 'date':
                self.line_edit_post_filter.setDate(datetime.datetime.strptime(self.column_property['postfilterArr'][0]['filterValue'], "%Y.%m.%d"))
        else:
            self.checkBox_widget_for_post_filter_check.setCheckState(QtCore.Qt.Unchecked)
            self.line_edit_post_filter.setDisabled(True)
            self.combo_box_post_filter_condition.setDisabled(True)
            self.widget_for_post_filter.setDisabled(True)

    def set_data_type_widget(self, index):
        if self.coltypes[index] == 'String':
            self.line_edit_post_filter = QtWidgets.QLineEdit()
        if self.coltypes[index] == 'Integer':
            self.line_edit_post_filter = QtWidgets.QSpinBox()
            self.line_edit_post_filter.setRange(-10000, 10000)
        if self.coltypes[index] == 'Float':
            self.line_edit_post_filter = QtWidgets.QDoubleSpinBox()
            self.line_edit_post_filter.setRange(-10000, 10000)
        if self.coltypes[index] == 'Date':
            self.line_edit_post_filter = QtWidgets.QDateEdit()
            self.line_edit_post_filter.setDisplayFormat("yyyy.MM.dd")
            self.line_edit_post_filter.setCalendarPopup(True)
        if self.coltypes[index] == '---':
            self.line_edit_post_filter = QtWidgets.QLineEdit()
            self.line_edit_post_filter.setText('---')

        if self.coltypes[index] != 'String':
            self.combo_box_post_filter_condition = QtWidgets.QComboBox()
            self.list_of_types_equals_for_filter = ['!=', '=', '>', '<', '<=', '>=']
            self.combo_box_post_filter_condition.addItems(self.list_of_types_equals_for_filter)
        if self.coltypes[index] == 'String':
            self.combo_box_post_filter_condition = QtWidgets.QComboBox()
            self.list_of_types_equals_for_filter = ['!=', '=']
            self.combo_box_post_filter_condition.addItems(self.list_of_types_equals_for_filter)
        if self.coltypes[index] == '---':
            self.combo_box_post_filter_condition = QtWidgets.QComboBox()
            list_of_post_filter_conditions = ['---']
            self.combo_box_post_filter_condition.addItems(list_of_post_filter_conditions)

        self.widget_for_post_filter = QtWidgets.QWidget()
        hbox_layout_post_filter = QtWidgets.QHBoxLayout()
        text_begin_for_addBegin_post_filter = QtWidgets.QLabel(self.adapter.take_translate('SourceColumnsConfigEditor', 'Condition'))
        text_end_for_addBegin_post_filter = QtWidgets.QLabel(self.adapter.take_translate('SourceColumnsConfigEditor', 'ValueCOLUMN'))
        hbox_layout_post_filter.addWidget(text_begin_for_addBegin_post_filter)
        hbox_layout_post_filter.addWidget(self.combo_box_post_filter_condition)
        hbox_layout_post_filter.addWidget(text_end_for_addBegin_post_filter)
        hbox_layout_post_filter.addWidget(self.line_edit_post_filter)
        self.widget_for_post_filter.setLayout(hbox_layout_post_filter)

        self.parent.setItemWidget(self, 1, self.widget_for_post_filter)

        self.checkBox_widget_for_post_filter_check.stateChanged.emit(1)