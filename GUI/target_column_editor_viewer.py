from PyQt5 import QtWidgets, QtCore
import sys



def create_receiver_column(tree_table: QtWidgets.QTreeWidget, db_colnames: list, column_property: dict, list_of_cols: list, index=None):
    tree_table.setColumnCount(2)
    tree_table.setHeaderLabels(['Property Name', 'Value'])

    list_in_comboBox_true_false = ['False', 'True']
    list_dict_to_comboBox = {'True': 'true', 'False': 'false'}

    combo_box_fromExcel = QtWidgets.QComboBox()
    combo_box_fromExcel.addItems(list_in_comboBox_true_false)

    combo_box_fromDb = QtWidgets.QComboBox()
    combo_box_fromDb.addItems(list_in_comboBox_true_false)

    combo_box_isAutoInc = QtWidgets.QComboBox()
    combo_box_isAutoInc.addItems(list_in_comboBox_true_false)

    combo_box_isConc = QtWidgets.QComboBox()
    combo_box_isConc.addItems(list_in_comboBox_true_false)

    combo_box_colType = QtWidgets.QComboBox()
    list_dict_to_comboBox_colType = {'String': 'str','Integer': 'int'}
    list_in_comboBox_colType = ['String''Integer']
    combo_box_colType.addItems(list_in_comboBox_colType)

    combo_box_isUpdateCondition = QtWidgets.QComboBox()
    combo_box_isUpdateCondition.addItems(list_in_comboBox_true_false)

    combo_box_ifNull = QtWidgets.QComboBox()
    combo_box_ifNull.addItems(list_in_comboBox_true_false)

    combo_box_reciever_names = QtWidgets.QComboBox()

    for name in db_colnames:
        combo_box_reciever_names.addItem(name)
    #
    # create tree widget item

    combo_box_reciever_names.setCurrentIndex(db_colnames.index(column_property['colName']))
    combo_box_fromExcel.setCurrentIndex(
        list_in_comboBox_true_false.index(list(filter(lambda x: list_dict_to_comboBox[x] == column_property['fromExcel'],
                                             list_dict_to_comboBox))[0])
    )

    combo_box_fromDb.setCurrentIndex()
    combo_box_isAutoInc.setCurrentIndex()
    combo_box_isConc.setCurrentIndex()
    combo_box_colType.setCurrentIndex()
    combo_box_isUpdateCondition.setCurrentIndex()
    combo_box_ifNull.setCurrentIndex()




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
