from PyQt5 import QtWidgets, QtCore
import sys


def create_receiver_column(tree_table: QtWidgets.QTreeWidget, column_property: dict, list_of_cols: list, adapter):
    tree_table.setColumnCount(2)
    tree_table.setHeaderLabels([adapter.take_translate('TargetColumnsConfigEditor', 'PropertyNameCOLUMN'),
                                adapter.take_translate('TargetColumnsConfigEditor', 'ValueCOLUMN')])
    dict_of_links = {}
    #
    # create tree widget item
    #

    colNameRow = ColumnnameReceiverRow(column_property, parent=tree_table, adapter=adapter)
    fromExcelRow = FromExcelStateRow(tree_table, column_property, colNameRow, adapter=adapter)
    fromDbStateRow = FromDbStateRow(tree_widget=tree_table, column_property=column_property, parent=colNameRow, adapter=adapter)
    isAutoIncStateRow = IsAutoIncStateRow(tree_table, column_property, colNameRow, adapter)
    isConcStateRow = IsConcStateRow(tree_table, column_property, colNameRow, adapter)
    colTypeRow = ColTypeRow(tree_table, column_property, colNameRow, adapter)
    isUpdateConditionRow = IsUpdateCondionRow(tree_table, column_property, colNameRow, adapter)
    defaultValue = DefaultValueRow(column_property=column_property, parent=tree_table, parent_widget=colNameRow, adapter=adapter)
    ifNullValue = IfNullRow(column_property=column_property, parent=tree_table, parent_widget=colNameRow, adapter=adapter)


    tree_table.addTopLevelItem(colNameRow)
    tree_table.addTopLevelItem(fromExcelRow)
    tree_table.addTopLevelItem(fromDbStateRow)
    tree_table.addTopLevelItem(isAutoIncStateRow)
    tree_table.addTopLevelItem(isConcStateRow)
    tree_table.addTopLevelItem(colTypeRow)
    tree_table.addTopLevelItem(isUpdateConditionRow)
    tree_table.addTopLevelItem(defaultValue)
    tree_table.addTopLevelItem(ifNullValue)

    fromDbStateRow.parent().child(0).checkBox.stateChanged.connect(fromDbStateRow.uncheck_checkbox)
    isAutoIncStateRow.parent().child(0).checkBox.stateChanged.connect(isAutoIncStateRow.uncheck_checkbox)
    defaultValue.parent().child(0).checkBox.stateChanged.connect(defaultValue.uncheck_checkbox)

    fromExcelRow.parent().child(1).checkBox.stateChanged.connect(fromExcelRow.uncheck_checkbox)
    isAutoIncStateRow.parent().child(1).checkBox.stateChanged.connect(isAutoIncStateRow.uncheck_checkbox)
    isConcStateRow.parent().child(1).checkBox.stateChanged.connect(isConcStateRow.uncheck_checkbox)
    defaultValue.parent().child(1).checkBox.stateChanged.connect(defaultValue.uncheck_checkbox)
    ifNullValue.parent().child(1).checkBox.stateChanged.connect(ifNullValue.uncheck_checkbox)
    isUpdateConditionRow.parent().child(1).checkBox.stateChanged.connect(isUpdateConditionRow.uncheck_checkbox)
    colTypeRow.parent().child(1).checkBox.stateChanged.connect(colTypeRow.uncheck_checkbox)

    fromExcelRow.parent().child(2).checkBox.stateChanged.connect(fromExcelRow.uncheck_checkbox)
    fromDbStateRow.parent().child(2).checkBox.stateChanged.connect(fromDbStateRow.uncheck_checkbox)
    isConcStateRow.parent().child(2).checkBox.stateChanged.connect(isConcStateRow.uncheck_checkbox)
    colTypeRow.parent().child(2).checkBox.stateChanged.connect(colTypeRow.uncheck_checkbox)
    isUpdateConditionRow.parent().child(2).checkBox.stateChanged.connect(isUpdateConditionRow.uncheck_checkbox)
    defaultValue.parent().child(2).checkBox.stateChanged.connect(defaultValue.uncheck_checkbox)
    ifNullValue.parent().child(2).checkBox.stateChanged.connect(ifNullValue.uncheck_checkbox)

    fromExcelRow.parent().child(3).checkBox.stateChanged.connect(fromExcelRow.check_check_box)
    isUpdateConditionRow.parent().child(3).checkBox.stateChanged.connect(isUpdateConditionRow.uncheck_checkbox)

    fromExcelRow.parent().child(6).checkBox_widget_for_defaultValue_check.stateChanged.connect(fromExcelRow.uncheck_checkbox)
    fromDbStateRow.parent().child(6).checkBox_widget_for_defaultValue_check.stateChanged.connect(fromDbStateRow.uncheck_checkbox)
    isAutoIncStateRow.parent().child(6).checkBox_widget_for_defaultValue_check.stateChanged.connect(isAutoIncStateRow.uncheck_checkbox)
    isConcStateRow.parent().child(6).checkBox_widget_for_defaultValue_check.stateChanged.connect(isConcStateRow.uncheck_checkbox)
    ifNullValue.parent().child(6).checkBox_widget_for_defaultValue_check.stateChanged.connect(ifNullValue.uncheck_checkbox)

    defaultValue.parent().child(7).checkBox_widget_for_ifNull_check.stateChanged.connect(defaultValue.uncheck_checkbox)


    if fromExcelRow.checkBox.isChecked():
        fromExcelRow.checkBox.stateChanged.emit(1)
    if fromDbStateRow.checkBox.isChecked():
        fromDbStateRow.checkBox.stateChanged.emit(1)
    if isAutoIncStateRow.checkBox.isChecked():
        isAutoIncStateRow.checkBox.stateChanged.emit(1)
    if isConcStateRow.checkBox.isChecked():
        isConcStateRow.checkBox.stateChanged.emit(1)

    dict_of_links['colNameRow'] = colNameRow
    dict_of_links['fromExcelRow'] = fromExcelRow
    dict_of_links['fromDbStateRow'] = fromDbStateRow
    dict_of_links['isAutoIncStateRow'] = isAutoIncStateRow
    dict_of_links['isConcStateRow'] = isConcStateRow
    dict_of_links['colTypeRow'] = colTypeRow
    dict_of_links['isUpdateConditionRow'] = isUpdateConditionRow
    dict_of_links['defaultValue'] = defaultValue
    dict_of_links['ifNullValue'] = ifNullValue

    list_of_cols.append(dict_of_links)



class ColumnnameReceiverRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget = None, adapter=None):
        super().__init__(parent, [adapter.take_translate('TargetColumnsConfigEditor', 'colName'), column_property['colName']])
        self.name = column_property['colName']
        self.col_name = column_property['colName']
        self.column_property = column_property

class FromExcelStateRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, column_property, parent=None, adapter=None):
        super().__init__(parent, [adapter.take_translate('TargetColumnsConfigEditor', 'fromExcel'),])
        list_dict_to_comboBox = {'True': 'true', 'False': 'false'}
        self.checkBox = QtWidgets.QCheckBox()

        state = list(filter(lambda x: list_dict_to_comboBox[x] == column_property['fromExcel'],
                            list_dict_to_comboBox))[0]

        if state == 'True':
            self.checkBox.setCheckState(QtCore.Qt.Checked)
        elif state == 'False':
            self.checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            raise SystemError('Unknown state')

        tree_widget.setItemWidget(self, 1, self.checkBox)


    def uncheck_checkbox(self, state):
        if state:
            self.checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.checkBox.setDisabled(True)
            self.setDisabled(True)
        else:
            self.checkBox.setDisabled(False)
            self.setDisabled(False)

    def check_check_box(self, state):
        if state:
            self.checkBox.setCheckState(QtCore.Qt.Checked)


class FromDbStateRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, column_property, parent=None, adapter=None):
        super().__init__(parent, [adapter.take_translate('TargetColumnsConfigEditor', 'fromDb'),])

        list_dict_to_comboBox = {'True': 'true', 'False': 'false'}
        self.checkBox = QtWidgets.QCheckBox()
        state = list(filter(lambda x: list_dict_to_comboBox[x] == column_property['fromDb'],
                            list_dict_to_comboBox))[0]
        if state == 'True':
            self.checkBox.setCheckState(QtCore.Qt.Checked)
        elif state == 'False':
            self.checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            raise SystemError('Unknown state')
        tree_widget.setItemWidget(self, 1, self.checkBox)


    def uncheck_checkbox(self, state):
        if state:
            self.checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.checkBox.setDisabled(True)
            self.setDisabled(True)
        else:
            self.checkBox.setDisabled(False)
            self.setDisabled(False)

class IsAutoIncStateRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, column_property, parent=None, adapter=None):
        super().__init__(parent, [adapter.take_translate('TargetColumnsConfigEditor', 'isAutoInc'), ])
        list_dict_to_comboBox = {'True': 'true', 'False': 'false'}
        self.checkBox = QtWidgets.QCheckBox()
        state = list(filter(lambda x: list_dict_to_comboBox[x] == column_property['isAutoInc'],
                            list_dict_to_comboBox))[0]
        if state == 'True':
            self.checkBox.setCheckState(QtCore.Qt.Checked)
        elif state == 'False':
            self.checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            raise SystemError('Unknown state')
        tree_widget.setItemWidget(self, 1, self.checkBox)


    def uncheck_checkbox(self, state):
        if state:
            self.checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.checkBox.setDisabled(True)
            self.setDisabled(True)
        else:
            self.checkBox.setDisabled(False)
            self.setDisabled(False)


class IsConcStateRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, column_property, parent=None, adapter=None):
        super().__init__(parent, [adapter.take_translate('TargetColumnsConfigEditor', 'isConc'), ])
        list_dict_to_comboBox = {'True': 'true', 'False': 'false'}
        self.checkBox = QtWidgets.QCheckBox()
        state = list(filter(lambda x: list_dict_to_comboBox[x] == column_property['isConc'],
                            list_dict_to_comboBox))[0]
        if state == 'True':
            self.checkBox.setCheckState(QtCore.Qt.Checked)
        elif state == 'False':
            self.checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            raise SystemError('Unknown state')
        tree_widget.setItemWidget(self, 1, self.checkBox)

    def uncheck_checkbox(self, state):
        if state:
            self.checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.checkBox.setDisabled(True)
            self.setDisabled(True)
        else:
            self.checkBox.setDisabled(False)
            self.setDisabled(False)



class ColTypeRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, column_property, parent=None, adapter=None):
        super().__init__(parent, [adapter.take_translate('TargetColumnsConfigEditor', 'colType'), ])
        self.combo_box_colType = QtWidgets.QComboBox()
        list_dict_to_comboBox_colType = {'String': 'str', 'Integer': 'int'}
        list_in_comboBox_colType = ['String', 'Integer']
        self.combo_box_colType.addItems(list_in_comboBox_colType)


        if column_property['colType'] in ['str', 'int']:
            self.combo_box_colType.setCurrentIndex(
                list_in_comboBox_colType.index(
                    list(filter(lambda x: list_dict_to_comboBox_colType[x] == column_property['colType'],
                                list_dict_to_comboBox_colType))[0])
            )
        else:
            self.combo_box_colType.addItem(column_property['colType'])
            self.combo_box_colType.setCurrentText(column_property['colType'])

        tree_widget.setItemWidget(self, 1, self.combo_box_colType)

    def uncheck_checkbox(self, state):
        if state:
            self.combo_box_colType.setDisabled(True)
            self.setDisabled(True)
        else:
            self.combo_box_colType.setDisabled(False)
            self.setDisabled(False)


class IsUpdateCondionRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, column_property, parent=None, adapter=None):
        super().__init__(parent, [adapter.take_translate('TargetColumnsConfigEditor', 'isUpdateCondition'), ])
        list_dict_to_comboBox = {'True': 'true', 'False': 'false'}
        self.checkBox = QtWidgets.QCheckBox()
        state = list(filter(lambda x: list_dict_to_comboBox[x] == column_property['isUpdateCondition'],
                            list_dict_to_comboBox))[0]
        if state == 'True':
            self.checkBox.setCheckState(QtCore.Qt.Checked)
        elif state == 'False':
            self.checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            raise SystemError('Unknown state')
        tree_widget.setItemWidget(self, 1, self.checkBox)

    def uncheck_checkbox(self, state):
        if state:
            self.checkBox.setCheckState(QtCore.Qt.Unchecked)
            self.checkBox.setDisabled(True)
            self.setDisabled(True)
        else:
            self.checkBox.setDisabled(False)
            self.setDisabled(False)



class DefaultValueRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget, adapter):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_defaultValue_check = QtWidgets.QCheckBox(adapter.take_translate('TargetColumnsConfigEditor', 'defaultValue'))

        self.line_edit_defeultValue = QtWidgets.QLineEdit()

        self.initialize()

        parent.setItemWidget(self, 0, self.checkBox_widget_for_defaultValue_check)
        parent.setItemWidget(self, 1, self.line_edit_defeultValue)
        self.checkBox_widget_for_defaultValue_check.stateChanged.connect(self.state_change)



    def uncheck_checkbox(self, state):
        if state:
            self.checkBox_widget_for_defaultValue_check.setCheckState(QtCore.Qt.Unchecked)
            self.checkBox_widget_for_defaultValue_check.setDisabled(True)
            self.line_edit_defeultValue.setDisabled(True)
            self.setDisabled(True)
        else:
            self.checkBox_widget_for_defaultValue_check.setDisabled(False)
            self.line_edit_defeultValue.setDisabled(False)
            self.setDisabled(False)

    def initialize(self):
        if self.column_property['defaultValue_mode'] != 'false':
            self.line_edit_defeultValue.setText(self.column_property['ifNull'])
            self.checkBox_widget_for_defaultValue_check.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBox_widget_for_defaultValue_check.setCheckState(QtCore.Qt.Unchecked)
            self.line_edit_defeultValue.setDisabled(True)

    def state_change(self):
        if self.checkBox_widget_for_defaultValue_check.isChecked():
            self.line_edit_defeultValue.setDisabled(False)
        else:
            self.line_edit_defeultValue.setDisabled(True)


class IfNullRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget, adapter):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_ifNull_check = QtWidgets.QCheckBox(adapter.take_translate('TargetColumnsConfigEditor', 'ifNull'))
        self.line_edit_ifNull = QtWidgets.QLineEdit()

        self.initialize()

        parent.setItemWidget(self, 0, self.checkBox_widget_for_ifNull_check)
        parent.setItemWidget(self, 1, self.line_edit_ifNull)
        self.checkBox_widget_for_ifNull_check.stateChanged.connect(self.state_change)

    def uncheck_checkbox(self, state):
        if state:
            self.checkBox_widget_for_ifNull_check.setCheckState(QtCore.Qt.Unchecked)
            self.checkBox_widget_for_ifNull_check.setDisabled(True)
            self.line_edit_ifNull.setDisabled(True)
            self.setDisabled(True)
        else:
            self.checkBox_widget_for_ifNull_check.setDisabled(False)
            self.line_edit_ifNull.setDisabled(False)
            self.setDisabled(False)

    def initialize(self):
        if self.column_property['ifNull_mode'] != 'false':
            self.line_edit_ifNull.setText(self.column_property['ifNull'])
            self.checkBox_widget_for_ifNull_check.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkBox_widget_for_ifNull_check.setCheckState(QtCore.Qt.Unchecked)
            self.line_edit_ifNull.setDisabled(True)

    def state_change(self):
        if self.checkBox_widget_for_ifNull_check.isChecked():
            self.line_edit_ifNull.setDisabled(False)
        else:
            self.line_edit_ifNull.setDisabled(True)
