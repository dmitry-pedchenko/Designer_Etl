import xml.etree.ElementTree as et
from PyQt5 import QtCore


class CreateXML(QtCore.QThread):
    error_message = QtCore.pyqtSignal(object)
    message = QtCore.pyqtSignal(object, object)

    def __init__(self
                 , obj
                 ) -> None:
        super().__init__()
        self.obj = obj

    def run(self):
        list_of_types_dict_to_comboBox = {
            'String': 'str',
            'Float': 'float',
            'Integer': 'int',
            'Date': 'date',
            '---': '---'
        }
        root = et.Element('main')
        tree = et.ElementTree(root)

        importXml = et.SubElement(root, 'importXml')
        importXml_columns = et.SubElement(importXml, 'columns')
        linkedColumns = et.SubElement(importXml, 'linkedColumns')
        withDict = et.SubElement(importXml, 'withDict')
        exportTable = et.SubElement(root, 'exportTable')
        exportTable_columns = et.SubElement(exportTable, 'columns')

        et.SubElement(root, 'dbtype').text = f'{self.obj.pref["dbtype"]}'
        et.SubElement(root, 'dbHost').text = f'{self.obj.pref["dbHost"]}'
        et.SubElement(root, 'dbSchema').text = f'{self.obj.pref["dbSchema"]}'
        et.SubElement(root, 'dbUser').text = f'{self.obj.pref["dbUser"]}'
        et.SubElement(root, 'dbPass').text = f'{self.obj.pref["dbPass"]}'
        et.SubElement(root, 'dbBase').text = f'{self.obj.pref["dbBase"]}'
        et.SubElement(root, 'dbPort').text = f'{self.obj.pref["dbPort"]}'
        et.SubElement(root, 'loadMode').text = f'{self.obj.pref["Load Mode"]}'.lower()
        et.SubElement(root, 'dict').text = f'{self.obj.pref["checkBox_Dictionary"]}'.lower()
        et.SubElement(root, 'checkMode').text = f'{self.obj.pref["checkBox_checkMode"]}'.lower()
        et.SubElement(importXml, 'path').text = f'{self.obj.pref["excelFileName"]}'
        et.SubElement(importXml, 'sheetNumber').text = f'{self.obj.pref["comboBox_list_source_excel"] + 1}'

        linkedColumns.attrib['mode'] = f'{self.obj.pref["checkBox_checkMode"]}'.lower()

        for column in self.obj.list_of_source_cols_links:
            column_to_add = et.SubElement(importXml_columns, 'column')

            et.SubElement(column_to_add, 'colName').text = column['colName'].combo_box_name.currentText()
            et.SubElement(column_to_add, 'colNameDb').text = column['colNameDb'].currentText()
            col_type = et.SubElement(column_to_add, 'colType').text = list_of_types_dict_to_comboBox[
                f'{column["colType"].currentText()}']
            et.SubElement(column_to_add, 'isPK').text = f"{column['isPK'].isChecked()}".lower()

            cropEnd = et.SubElement(column_to_add, 'cropEnd')
            if column['cropEnd_box'].checkBox_widget_for_cropEnd_check.isChecked():
                cropEnd.text = f"{column['cropEnd_box'].spin_box_cropEnd.value()}"
            cropEnd.attrib['mode'] = \
                f"{column['cropEnd_box'].checkBox_widget_for_cropEnd_check.isChecked()}".lower()

            addValueEnd = et.SubElement(column_to_add, 'addValueEnd')
            if column['addValueEnd_box'].checkBox_widget_for_addValueEnd_check.isChecked():
                addValueEnd.text = f"{column['addValueEnd_box'].line_edit_addValueEnd.text()}"
            addValueEnd.attrib['mode'] = \
                f"{column['addValueEnd_box'].checkBox_widget_for_addValueEnd_check.isChecked()}".lower()

            takeFromBegin = et.SubElement(column_to_add, 'takeFromBegin')
            if column['takeFromBegin_box'].checkBox_widget_for_takeFromBegin_check.isChecked():
                takeFromBegin.text = f"{column['takeFromBegin_box'].spin_box_takeFromBegin.value()}"
            takeFromBegin.attrib['mode'] = \
                f"{column['takeFromBegin_box'].checkBox_widget_for_takeFromBegin_check.isChecked()}".lower()

            cropBegin = et.SubElement(column_to_add, 'cropBegin')
            if column['cropBegin_box'].checkBox_widget_for_cropBegin_check.isChecked():
                cropBegin.text = f"{column['cropBegin_box'].spin_box_cropBegin.value()}"
            cropBegin.attrib['mode'] = \
                f"{column['cropBegin_box'].checkBox_widget_for_cropBegin_check.isChecked()}".lower()

            addValueBegin = et.SubElement(column_to_add, 'addValueBegin')
            if column['addValueBegin_box'].checkBox_widget_for_addValueBegin_check.isChecked():
                addValueBegin.text = f"{column['addValueBegin_box'].line_edit_addValueBegin.text()}"
            addValueBegin.attrib['mode'] = \
                f"{column['addValueBegin_box'].checkBox_widget_for_addValueBegin_check.isChecked()}".lower()

            addValueBoth = et.SubElement(column_to_add, 'addValueBoth')
            if column['addValueBoth_box'].checkBox_widget_for_addValueBoth_check.isChecked():
                addValueBoth.text = \
                    f"{column['addValueBoth_box'].line_edit_addBegin_Both_filter.text()},{column['addValueBoth_box'].line_edit_addEnd_Both_filter.text()}"
            addValueBoth.attrib['mode'] = \
                f"{column['addValueBoth_box'].checkBox_widget_for_addValueBoth_check.isChecked()}".lower()

            replace_box = et.SubElement(column_to_add, 'replace')

            for replace in column['replace_box']:
                if replace.checkBox_widget_for_replace_check.isChecked():
                    replace_box.attrib['mode'] = 'true'

                    replaceVal = et.SubElement(replace_box, 'replaceVal')

                    et.SubElement(replaceVal, 'value').text = f"""{replace.line_edit_addBegin_Both.text()}"""
                    et.SubElement(replaceVal, 'toValue').text = f"""{replace.line_edit_addEnd_Both.text()}"""
                else:
                    replace_box.attrib['mode'] = 'false'

            filter_box = et.SubElement(column_to_add, 'filter')
            if column['filter_box'].checkBox_widget_for_filter_check.isChecked():
                filter_box.attrib['mode'] = 'true'

                f_cropEnd = et.SubElement(filter_box, 'f_cropEnd')
                if column['filter_box'].checkBox_widget_f_cropEnd_check.isChecked():
                    f_cropEnd.text = f'{column["filter_box"].spin_box_f_cropEnd.value()}'
                f_cropEnd.attrib['mode'] = \
                    f'{column["filter_box"].checkBox_widget_f_cropEnd_check.isChecked()}'.lower()

                f_addValueEnd = et.SubElement(filter_box, 'f_addValueEnd')
                if column['filter_box'].checkBox_widget_f_addValueEnd_check.isChecked():
                    f_addValueEnd.text = f'{column["filter_box"].line_edit_f_addValueEnd.text()}'
                f_addValueEnd.attrib['mode'] = \
                    f'{column["filter_box"].checkBox_widget_f_addValueEnd_check.isChecked()}'.lower()

                f_takeFromBegin = et.SubElement(filter_box, 'f_takeFromBegin')
                if column['filter_box'].checkBox_widget_f_takeFromBegin_check.isChecked():
                    f_takeFromBegin.text = f'{column["filter_box"].spin_box_f_takeFromBegin.value()}'
                f_takeFromBegin.attrib['mode'] = \
                    f'{column["filter_box"].checkBox_widget_f_takeFromBegin_check.isChecked()}'.lower()

                f_cropBegin = et.SubElement(filter_box, 'f_cropBegin')
                if column['filter_box'].checkBox_widget_f_cropBegin_check.isChecked():
                    f_cropBegin.text = f'{column["filter_box"].spin_box_f_cropBegin.value()}'
                f_cropBegin.attrib['mode'] = \
                    f'{column["filter_box"].checkBox_widget_f_cropBegin_check.isChecked()}'.lower()

                f_addValueBegin = et.SubElement(filter_box, 'f_addValueBegin')
                if column['filter_box'].checkBox_widget_f_addValueBegin_check.isChecked():
                    f_addValueBegin.text = f'{column["filter_box"].line_edit_f_addValueBegin.text()}'
                f_addValueBegin.attrib['mode'] = \
                    f'{column["filter_box"].checkBox_widget_f_addValueBegin_check.isChecked()}'.lower()

                f_addValueBoth = et.SubElement(filter_box, 'f_addValueBoth')
                if column['filter_box'].checkBox_widget_f_addValueBoth_check.isChecked():
                    f_addValueBoth.text = f'{column["filter_box"].line_edit_addBegin_Both_filter.text()},{column["filter_box"].line_edit_addEnd_Both_filter.text()}'
                f_addValueBoth.attrib['mode'] = \
                    f'{column["filter_box"].checkBox_widget_f_addValueBoth_check.isChecked()}'.lower()

                filterVal = et.SubElement(filter_box, 'filterVal')
                filterMode = et.SubElement(filterVal, 'filterMode')
                filterValue = et.SubElement(filterVal, 'filterValue')


                if column['filter_box'].combo_box_filter_condition.currentText() == '---':
                    self.error_message.emit(f"Filter mode must be not '---' !!!")
                    return

                filterMode.text = f"{column['filter_box'].combo_box_filter_condition.currentText()}"

                if col_type == 'str':
                    filterValue.text = column['filter_box'].line_edit_addEnd_filter.text()
                elif col_type == 'int' or col_type == 'float':
                    filterValue.text = column['filter_box'].line_edit_addEnd_filter.value()
                elif col_type == 'date':
                    filterValue.text = column['filter_box'].line_edit_addEnd_filter.date().toPyDate().strftime("%Y.%m.%d")
                else:
                    self.obj.loggerInst.raiseError(0, 'Unknown filter type')

            else:
                filter_box.attrib['mode'] = 'false'

            post_filter = et.SubElement(column_to_add, 'post-filter')

            if column['post_filter_box'].checkBox_widget_for_post_filter_check.isChecked():
                post_filter.attrib['mode'] = 'true'

                filterMode = et.SubElement(post_filter, 'filterMode')
                filterValue = et.SubElement(post_filter, 'filterValue')

                filterMode.text = f"{column['post_filter_box'].combo_box_post_filter_condition.currentText()}"

                if col_type == 'str':
                    filterValue.text = column['post_filter_box'].line_edit_post_filter.text()
                elif col_type == 'int' or col_type == 'float':
                    filterValue.text = column['post_filter_box'].line_edit_post_filter.value()
                elif col_type == 'date':
                    filterValue.text = column['post_filter_box'].line_edit_post_filter.date().toPyDate().strftime(
                        "%Y.%m.%d")
                else:
                    self.obj.loggerInst.raiseError(0, 'Unknown filter type')
            else:
                post_filter.attrib['mode'] = 'false'

        if hasattr(self.obj.pref_gui, "ui"):
            if self.obj.pref_gui.ui.checkBox_checkMode.isChecked():
                pathToLinkFile = et.SubElement(linkedColumns, 'pathToLinkFile')
                pathToLinkFile.text = f"{self.obj.pref_gui.ui.compare_file.text()}"
                linkedFileSheetNumber = et.SubElement(linkedColumns, 'linkedFileSheetNumber')
                linkedFileSheetNumber.text = f"{self.obj.pref_gui.comboBox_set_list_checked.currentIndex() + 1}"
                both = et.SubElement(linkedColumns, 'both')
                both.text = f"{self.obj.pref_gui.ui.checkBox_both.isChecked()}".lower()

                for col in self.obj.pref['col_to_check']:
                    column = et.SubElement(linkedColumns, 'column')
                    linkedColName = et.SubElement(column, 'linkedColName')
                    colNameInSource = et.SubElement(column, 'colNameInSource')

                    colNameInSource.text = f"{col.combo_box_source_links.currentText()}"
                    linkedColName.text = f"{col.combo_box_target_links.currentText()}"
        else:
            if self.obj.pref_gui.checkBox_checkMode.isChecked():
                pathToLinkFile = et.SubElement(linkedColumns, 'pathToLinkFile')
                pathToLinkFile.text = f"{self.obj.pref_gui.compare_file.text()}"
                linkedFileSheetNumber = et.SubElement(linkedColumns, 'linkedFileSheetNumber')
                linkedFileSheetNumber.text = f"{self.obj.pref_gui.comboBox_set_list_checked.currentIndex() + 1}"
                both = et.SubElement(linkedColumns, 'both')
                both.text = f"{self.obj.pref_gui.checkBox_both.isChecked()}".lower()

                for col in self.obj.pref['col_to_check']:
                    column = et.SubElement(linkedColumns, 'column')
                    linkedColName = et.SubElement(column, 'linkedColName')
                    colNameInSource = et.SubElement(column, 'colNameInSource')

                    colNameInSource.text = f"{col.combo_box_source_links.currentText()}"
                    linkedColName.text = f"{col.combo_box_target_links.currentText()}"


        if hasattr(self.obj.pref_gui, "ui"):
            checkBox_Dictionary = self.obj.pref_gui.ui.checkBox_Dictionary
        else:
            checkBox_Dictionary = self.obj.pref_gui.checkBox_Dictionary

        if checkBox_Dictionary.isChecked():
            tables = et.SubElement(withDict, 'tables')
            withDict.attrib['mode'] = 'true'

            for table_count in self.obj.list_of_dict_pref:
                table = et.SubElement(tables, 'table')
                dictTableName = et.SubElement(table, 'dictTableName')
                dictTableName.text = table_count["dictTableName"].combo_box_dictTableName.currentText()
                indxDbColumn = et.SubElement(table, 'indxDbColumn')
                indxDbColumn.text = table_count["indxDbColumn"].combo_box_indxDbColumn.currentText()
                indxColumnDic = et.SubElement(table, 'indxColumnDic')
                indxColumnDic.text = table_count["indxColumnDic"].combo_box_indxColumnDic.currentText()

                columns = et.SubElement(table, 'columns')

                for col_count in table_count['columns']:
                    column = et.SubElement(columns, 'column')

                    colName = et.SubElement(column, 'colName')
                    colName.text = col_count['colNameRow'].combo_box.currentText()

                    colNameDb = et.SubElement(column, 'colNameDb')
                    colNameDb.text = col_count['colNameDbRow'].combo_box_colnameDb.currentText()

                    colType = et.SubElement(column, 'colType')
                    colType.text = list_of_types_dict_to_comboBox[
                        f"{col_count['colTypeRow'].combo_box_colType.currentText()}"]

                    cropEnd = et.SubElement(column, 'cropEnd')
                    if col_count['cropEndRow'].checkBox_widget_for_cropEnd_check.isChecked():
                        cropEnd.text = f'{col_count["cropEndRow"].spin_box_cropEnd.value()}'
                    cropEnd.attrib['mode'] = \
                        f'{col_count["cropEndRow"].checkBox_widget_for_cropEnd_check.isChecked()}'.lower()

                    addValueEnd = et.SubElement(column, 'addValueEnd')
                    if col_count['addValueEndRow'].checkBox_widget_for_addValueEnd_check.isChecked():
                        addValueEnd.text = f'{col_count["addValueEndRow"].line_edit_addValueEnd.text()}'
                    addValueEnd.attrib['mode'] = \
                        f'{col_count["addValueEndRow"].checkBox_widget_for_addValueEnd_check.isChecked()}'.lower()

                    takeFromBegin = et.SubElement(column, 'takeFromBegin')
                    if col_count['takeFromBeginRow'].checkBox_widget_for_takeFromBegin_check.isChecked():
                        takeFromBegin.text = f'{col_count["takeFromBeginRow"].spin_box_takeFromBegin.value()}'
                    takeFromBegin.attrib['mode'] = \
                        f'{col_count["takeFromBeginRow"].checkBox_widget_for_takeFromBegin_check.isChecked()}'.lower()

                    cropBegin = et.SubElement(column, 'cropBegin')
                    if col_count['cropBeginRow'].checkBox_widget_for_cropBegin_check.isChecked():
                        cropBegin.text = f'{col_count["cropBeginRow"].spin_box_cropBegin.value()}'
                    cropBegin.attrib['mode'] = \
                        f'{col_count["cropBeginRow"].checkBox_widget_for_cropBegin_check.isChecked()}'.lower()

                    addValueBegin = et.SubElement(column, 'addValueBegin')
                    if col_count['addValueBeginRow'].checkBox_widget_for_addValueBegin_check.isChecked():
                        addValueBegin.text = f'{col_count["addValueBeginRow"].line_edit_addValueBegin.text()}'
                    addValueBegin.attrib['mode'] = \
                        f'{col_count["addValueBeginRow"].checkBox_widget_for_addValueBegin_check.isChecked()}'.lower()

                    addValueBoth = et.SubElement(column, 'addValueBoth')
                    if col_count['addValueBothRow'].checkBox_widget_for_addValueBoth_check.isChecked():
                        addValueBoth.text = f'{col_count["addValueBothRow"].line_edit_addBegin_Both_filter.text()},{col_count["addValueBothRow"].line_edit_addEnd_Both_filter.text()}'
                    addValueBoth.attrib['mode'] = \
                        f'{col_count["addValueBothRow"].checkBox_widget_for_addValueBoth_check.isChecked()}'.lower()

                    replace_box = et.SubElement(column, 'replace')

                    for replace in col_count['replace_box']:
                        if replace.checkBox_widget_for_replace_check.isChecked():
                            replace_box.attrib['mode'] = 'true'

                            replaceVal = et.SubElement(replace_box, 'replaceVal')

                            et.SubElement(replaceVal, 'value').text = f"""{replace.line_edit_addBegin_Both.text()}"""
                            et.SubElement(replaceVal, 'toValue').text = f"""{replace.line_edit_addEnd_Both.text()}"""
                        else:
                            replace_box.attrib['mode'] = 'false'
        else:
            withDict.attrib['mode'] = 'false'

        path = et.SubElement(exportTable, 'path')
        path.text = f"{self.obj.pref['target_table_name']}"

        for col in self.obj.list_of_receiver_cols_links:
            column = et.SubElement(exportTable_columns, 'column')

            name = et.SubElement(column, 'name')
            name.text = col['colNameRow'].name
            fromExcel = et.SubElement(column, 'fromExcel')
            fromExcel.text = f"{col['fromExcelRow'].checkBox.isChecked()}".lower()
            fromDb = et.SubElement(column, 'fromDb')
            fromDb.text = f"{col['fromDbStateRow'].checkBox.isChecked()}".lower()
            isAutoInc = et.SubElement(column, 'isAutoInc')
            isAutoInc.text = f"{col['isAutoIncStateRow'].checkBox.isChecked()}".lower()
            isConc = et.SubElement(column, 'isConc')
            isConc.text = f"{col['isConcStateRow'].checkBox.isChecked()}".lower()
            defaultValue = et.SubElement(column, 'defaultValue')

            if col['defaultValue'].checkBox_widget_for_defaultValue_check.isChecked():
                defaultValue.attrib['mode'] = 'true'
                defaultValue.text = col['defaultValue'].line_edit_defeultValue.text()
            else:
                defaultValue.attrib['mode'] = 'false'
            colType = et.SubElement(column, 'colType')
            colType.text = list_of_types_dict_to_comboBox[f"{col['colTypeRow'].combo_box_colType.currentText()}"]

            isUpdateCondition = et.SubElement(column, 'isUpdateCondition')
            isUpdateCondition.text = f"{col['isUpdateConditionRow'].checkBox.isChecked()}".lower()
            ifNull = et.SubElement(column, 'ifNull')
            if col['ifNullValue'].checkBox_widget_for_ifNull_check.isChecked():
                ifNull.attrib['mode'] = 'true'
                ifNull.text = f"{col['ifNullValue'].line_edit_ifNull.text()}"
            else:
                ifNull.attrib['mode'] = 'false'

        # tree.write(f"{self.path_config}")
        self.message.emit(tree, root)

