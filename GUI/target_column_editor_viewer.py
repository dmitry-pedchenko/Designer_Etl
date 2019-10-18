from PyQt5 import QtWidgets, QtCore
import sys


def create_receiver_column(tree_table: QtWidgets.QTreeWidget, db_colnames: list, column_property: dict, list_of_cols: list, index=None):
    tree_table.setColumnCount(2)
    tree_table.setHeaderLabels(['Property Name', 'Value'])

    #
    # create tree widget item
    #

    colNameRow = ColumnnameReceiverRow(column_property, parent=tree_table)
    fromExcelRow = FromExcelStateRow(tree_table, column_property, colNameRow)
    fromDbStateRow = FromDbStateRow(tree_table, column_property, colNameRow)
    isAutoIncStateRow = IsAutoIncStateRow(tree_table, column_property, colNameRow)
    isConcStateRow = IsConcStateRow(tree_table, column_property, colNameRow)
    colTypeRow = ColTypeRow(tree_table, column_property, colNameRow)
    isUpdateConditionRow = IsUpdateCondionRow(tree_table, column_property, colNameRow)
    defaultValue = DefaultValueRow(column_property=column_property,parent=tree_table,parent_widget=colNameRow)
    ifNullValue = IfNullRow(column_property=column_property,parent=tree_table,parent_widget=colNameRow)


    tree_table.addTopLevelItem(colNameRow)
    tree_table.addTopLevelItem(fromExcelRow)
    tree_table.addTopLevelItem(fromDbStateRow)
    tree_table.addTopLevelItem(isAutoIncStateRow)
    tree_table.addTopLevelItem(isConcStateRow)
    tree_table.addTopLevelItem(colTypeRow)
    tree_table.addTopLevelItem(isUpdateConditionRow)
    tree_table.addTopLevelItem(defaultValue)
    tree_table.addTopLevelItem(ifNullValue)




class ColumnnameReceiverRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget = None):
        super().__init__(parent, ["colName", column_property['colName']])

        self.col_name = column_property['colName']
        self.column_property = column_property

class FromExcelStateRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, column_property, parent=None):
        super().__init__(parent, ['fromExcel',])
        list_dict_to_comboBox = {'True': 'true', 'False': 'false'}

        checkBox = QtWidgets.QCheckBox()

        state = list(filter(lambda x: list_dict_to_comboBox[x] == column_property['fromExcel'],
                            list_dict_to_comboBox))[0]

        if state == 'True':
            checkBox.setCheckState(QtCore.Qt.Checked)
        elif state == 'False':
            checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            raise SystemError('Unknown state')

        tree_widget.setItemWidget(self, 1, checkBox)


class FromDbStateRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, column_property, parent=None):
        super().__init__(parent, ['fromDb',])
        list_dict_to_comboBox = {'True': 'true', 'False': 'false'}
        checkBox = QtWidgets.QCheckBox()
        state = list(filter(lambda x: list_dict_to_comboBox[x] == column_property['fromDb'],
                            list_dict_to_comboBox))[0]
        if state == 'True':
            checkBox.setCheckState(QtCore.Qt.Checked)
        elif state == 'False':
            checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            raise SystemError('Unknown state')
        tree_widget.setItemWidget(self, 1, checkBox)


class IsAutoIncStateRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, column_property, parent=None):
        super().__init__(parent, ['isAutoInc', ])
        list_dict_to_comboBox = {'True': 'true', 'False': 'false'}
        checkBox = QtWidgets.QCheckBox()
        state = list(filter(lambda x: list_dict_to_comboBox[x] == column_property['isAutoInc'],
                            list_dict_to_comboBox))[0]
        if state == 'True':
            checkBox.setCheckState(QtCore.Qt.Checked)
        elif state == 'False':
            checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            raise SystemError('Unknown state')
        tree_widget.setItemWidget(self, 1, checkBox)


class IsConcStateRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, column_property, parent=None):
        super().__init__(parent, ['isConc', ])
        list_dict_to_comboBox = {'True': 'true', 'False': 'false'}
        checkBox = QtWidgets.QCheckBox()
        state = list(filter(lambda x: list_dict_to_comboBox[x] == column_property['isConc'],
                            list_dict_to_comboBox))[0]
        if state == 'True':
            checkBox.setCheckState(QtCore.Qt.Checked)
        elif state == 'False':
            checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            raise SystemError('Unknown state')
        tree_widget.setItemWidget(self, 1, checkBox)




class ColTypeRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, column_property, parent=None):
        super().__init__(parent, ['colType', ])
        combo_box_colType = QtWidgets.QComboBox()
        list_dict_to_comboBox_colType = {'String': 'str', 'Integer': 'int'}
        list_in_comboBox_colType = ['String', 'Integer']
        combo_box_colType.addItems(list_in_comboBox_colType)

        combo_box_colType.setCurrentIndex(
            list_in_comboBox_colType.index(
                list(filter(lambda x: list_dict_to_comboBox_colType[x] == column_property['colType'],
                            list_dict_to_comboBox_colType))[0])
        )

        tree_widget.setItemWidget(self, 1, combo_box_colType)


class IsUpdateCondionRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, column_property, parent=None):
        super().__init__(parent, ['isUpdateCondition', ])
        list_dict_to_comboBox = {'True': 'true', 'False': 'false'}
        checkBox = QtWidgets.QCheckBox()
        state = list(filter(lambda x: list_dict_to_comboBox[x] == column_property['isUpdateCondition'],
                            list_dict_to_comboBox))[0]
        if state == 'True':
            checkBox.setCheckState(QtCore.Qt.Checked)
        elif state == 'False':
            checkBox.setCheckState(QtCore.Qt.Unchecked)
        else:
            raise SystemError('Unknown state')
        tree_widget.setItemWidget(self, 1, checkBox)


class DefaultValueRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_defaultValue_check = QtWidgets.QCheckBox('defaultValue')

        self.line_edit_defeultValue = QtWidgets.QLineEdit()

        parent.setItemWidget(self, 0, self.checkBox_widget_for_defaultValue_check)
        parent.setItemWidget(self, 1, self.line_edit_defeultValue)

class IfNullRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, column_property: dict, parent: QtWidgets.QTreeWidget, parent_widget):
        super().__init__(parent_widget, ['', ])
        self.column_property = column_property
        self.checkBox_widget_for_ifNull_check = QtWidgets.QCheckBox('ifNull')
        self.line_edit_ifNull = QtWidgets.QLineEdit()
        parent.setItemWidget(self, 0, self.checkBox_widget_for_ifNull_check)
        parent.setItemWidget(self, 1, self.line_edit_ifNull)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
