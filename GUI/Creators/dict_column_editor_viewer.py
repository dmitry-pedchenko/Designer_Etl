from PyQt5 import QtWidgets, QtCore


def create_dict_column(
        pref,
        parent,
        config,
        validator,
        tables_in_receiver,
        columns_names_source,
        cur_dic_table_pref,
        dbtype=None,
        target_table=None,
        db_base=None,
        connector=None,
        executor=None,
        cur=None,
        loggerInst=None,
        adapter=None
        ):
    dict_pref = {}
    dict_pref['columns'] = []

    if not isinstance(validator, type):
        columns_in_receiver = validator.queryForColumns()
    else:
        columns_in_receiver = validator.queryForColumns_edit(
            dbtype=dbtype,
            target_table=target_table,
            db_base=db_base,
            connector=connector,
            executor=executor,
            cur=cur,
            loggerInst=loggerInst
        )

    if cur_dic_table_pref['dictTableName']:
        columns_in_db_dict = validator.queryForColumnsInDict(cur_dic_table_pref['dictTableName'])
    else:
        columns_in_db_dict = None

    main_row = MainDictTableName(
        cur_dic_table_pref=cur_dic_table_pref,
        parent=parent,
        config=config,
        tables_in_receiver=tables_in_receiver,
        adapter=adapter
    )
    dict_pref_indxDbColumn = IndxDbColumn(
        cur_dic_table_pref=cur_dic_table_pref,
        parent=main_row,
        tree_widget=parent,
        config=config,
        columns_in_receiver=columns_in_receiver,
        adapter=adapter
    )
    dict_pref_indxColumnDic = IndxColumnDic(
        cur_dic_table_pref=cur_dic_table_pref,
        parent=main_row,
        tree_widget=parent,
        config=config,
        col_names_in_db_dict=columns_in_db_dict,
        table_name=main_row.combo_box_dictTableName,
        validator=validator,
        dbtype=dbtype,
        dbBase=db_base,
        connector=connector,
        executor=executor,
        target_table=target_table,
        cur=cur,
        loggerInst=loggerInst,
        adapter=adapter

    )

    if cur_dic_table_pref['arrOfDictColumns']:
        for row in cur_dic_table_pref['arrOfDictColumns']:
            temp_dict = {}
            temp_dict['replace_box'] = []

            colNameRow = ColumnNameRow(
                column_property=row,
                parent=main_row,
                tree_widget=parent,
                columns_names_source=columns_names_source,
                after_widget=dict_pref_indxColumnDic,
                adapter=adapter
            )
            colNameDbRow = ColumnNameDbRow(
                                    row,
                                    colNameRow,
                                    parent,
                                    columns_in_receiver=columns_in_db_dict,
                                    adapter=adapter,
                                    table_name=main_row.combo_box_dictTableName,
                                    validator=validator,
                                    dbtype=dbtype,
                                    db_base=db_base,
                                    connector=connector,
                                    executor=executor,
                                    cur=cur,
                                    loggerInst=loggerInst
            )
            colTypeRow = ColTypeRow(row, colNameRow, tree_widget=parent, adapter=adapter)
            cropEndRow = CropEndRow(row, parent, colNameRow, adapter)
            addValueEndRow = AddValueEndRow(row, parent, colNameRow, adapter)
            takeFromBeginRow = TakeFromBeginRow(row, parent, colNameRow, adapter)
            cropBeginRow = CropBeginRow(row, parent, colNameRow, adapter)
            addValueBeginRow = AddValueBeginRow(row, parent, colNameRow, adapter)
            addValueBothRow = AddValueBothRow(row, parent, colNameRow, adapter)

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
                            table_item=main_row,
                            adapter=adapter
                        )
                    else:
                        replace_box = ReplaceRow(
                            row=replace,
                            column_property=row,
                            parent=parent,
                            parent_widget=colNameRow,
                            after_widget=addValueBothRow,
                            table_item=main_row,
                            adapter=adapter
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
                            table_item=main_row,
                            adapter=adapter
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
    else:
        temp_dict = {}
        temp_dict['replace_box'] = []

        colNameRow = ColumnNameRow(
            column_property=cur_dic_table_pref,
            parent=main_row,
            tree_widget=parent,
            columns_names_source=columns_names_source,
            after_widget=dict_pref_indxColumnDic,
            adapter=adapter)
        colNameDbRow = ColumnNameDbRow(
            cur_dic_table_pref,
            colNameRow,
            parent,
            columns_in_receiver=columns_in_db_dict,
            adapter=adapter,
            table_name=main_row.combo_box_dictTableName,
            validator=validator,
            dbtype=dbtype,
            db_base=db_base,
            connector=connector,
            executor=executor,
            cur=cur,
            loggerInst=loggerInst)
        colTypeRow = ColTypeRow(cur_dic_table_pref, colNameRow, tree_widget=parent, adapter=adapter)
        cropEndRow = CropEndRow(cur_dic_table_pref, parent, colNameRow, adapter)
        addValueEndRow = AddValueEndRow(cur_dic_table_pref, parent, colNameRow, adapter)
        takeFromBeginRow = TakeFromBeginRow(cur_dic_table_pref, parent, colNameRow, adapter)
        cropBeginRow = CropBeginRow(cur_dic_table_pref, parent, colNameRow, adapter)
        addValueBeginRow = AddValueBeginRow(cur_dic_table_pref, parent, colNameRow, adapter)
        addValueBothRow = AddValueBothRow(cur_dic_table_pref, parent, colNameRow, adapter)


        replace_box = ReplaceRow(
            row=None,
            column_property=cur_dic_table_pref,
            parent=parent,
            parent_widget=colNameRow,
            after_widget=addValueBothRow,
            table_item=main_row,
            adapter= adapter
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
    iterator = 0
    def __init__(self, cur_dic_table_pref, parent, config, tables_in_receiver, adapter):
        super().__init__(parent, [adapter.take_translate('DictionaryEditor', 'table'), ])
        self.cur_dic_table_pref = cur_dic_table_pref
        self.objectName = 'table'
        list_combo_box_dictTableName = tables_in_receiver
        self.combo_box_dictTableName = QtWidgets.QComboBox()
        self.combo_box_dictTableName.addItems(sorted(list_combo_box_dictTableName))
        self.combo_box_dictTableName.addItem('---')
        self.unique_name = f"{MainDictTableName}_{MainDictTableName.iterator}"
        MainDictTableName.iterator = MainDictTableName.iterator + 1

        if cur_dic_table_pref['dictTableName']:
            self.combo_box_dictTableName.setCurrentIndex(sorted(list_combo_box_dictTableName).index(cur_dic_table_pref['dictTableName']))
        else:
            self.combo_box_dictTableName.setCurrentText('---')
        parent.setItemWidget(self, 1, self.combo_box_dictTableName)





class IndxDbColumn(QtWidgets.QTreeWidgetItem):
    def __init__(self, cur_dic_table_pref, parent, tree_widget, config, columns_in_receiver, adapter):
        super().__init__(parent, [adapter.take_translate('DictionaryEditor', 'indxDbColumn'), ])
        list_indxDbColumn = [i[0] for i in columns_in_receiver]
        self.combo_box_indxDbColumn = QtWidgets.QComboBox()
        self.combo_box_indxDbColumn.addItems(list_indxDbColumn)
        if cur_dic_table_pref['indxDbColumn']:
            self.combo_box_indxDbColumn.setCurrentIndex(list_indxDbColumn.index(cur_dic_table_pref['indxDbColumn']))
        tree_widget.setItemWidget(self, 1, self.combo_box_indxDbColumn)


class IndxColumnDic(QtWidgets.QTreeWidgetItem):
    def __init__(
            self,
            cur_dic_table_pref,
            parent,
            tree_widget,
            config,
            col_names_in_db_dict,
            table_name,
            validator,
            dbtype=None,
            dbBase=None,
            connector=None,
            executor=None,
            target_table=None,
            cur=None,
            loggerInst=None,
            adapter=None
            ):
        super().__init__(parent, [adapter.take_translate('DictionaryEditor', 'indxColumnDic'), ])
        self.dbtype = dbtype
        self.dbBase = dbBase
        self.connector = connector
        self.executor = executor
        self.target_table = target_table
        self.cur = cur
        self.loggerInst = loggerInst
        #
        self.validator = validator
        self.table_name=table_name
        if col_names_in_db_dict:
            list_indxColumnDic = [i[0] for i in col_names_in_db_dict]
        else:
            list_indxColumnDic = '---'
        #
        self.combo_box_indxColumnDic = QtWidgets.QComboBox()
        if col_names_in_db_dict:
            self.combo_box_indxColumnDic.addItems(list_indxColumnDic)
        else:
            self.combo_box_indxColumnDic.addItem(list_indxColumnDic)
        if cur_dic_table_pref['indxColumnDic']:
            self.combo_box_indxColumnDic.setCurrentIndex(list_indxColumnDic.index(cur_dic_table_pref['indxColumnDic']))
        tree_widget.setItemWidget(self, 1, self.combo_box_indxColumnDic)

        self.table_name.currentTextChanged.connect(self.cur_table_change)

    def cur_table_change(self, name):
        if not isinstance(self.validator, type):
            col_names_in_db_dict = self.validator.queryForColumnsInDict(f'{name}')
        else:
            col_names_in_db_dict = self.validator.queryForColumnsInDict_edit(
                dict_table_name=f"{name}",
                dbtype=self.dbtype,
                dbBase=self.dbBase,
                connector=self.connector,
                exec=self.executor,
                cur=self.cur,
                loggerInst=self.loggerInst
            )

        list_indxColumnDic = [i[0] for i in col_names_in_db_dict]

        while self.combo_box_indxColumnDic.count()>0:
            self.combo_box_indxColumnDic.removeItem(0)
        self.combo_box_indxColumnDic.addItems(list_indxColumnDic)


class ColTypeRow(QtWidgets.QTreeWidgetItem):
    def __init__(self, cur_dic_table_pref, parent, tree_widget, adapter):
        super().__init__(parent, [adapter.take_translate('SourceColumnsConfigEditor', 'colType'), ])

        list_of_types_dict_to_comboBox = {'String': 'str', 'Float': 'float', 'Integer': 'int', 'Date': 'date'}
        list_of_coltypes_in_comboBox = ['String', 'Float', 'Integer', 'Date']

        self.combo_box_colType = QtWidgets.QComboBox()
        self.combo_box_colType.addItems(list_of_coltypes_in_comboBox)

        tree_widget.setItemWidget(self, 1, self.combo_box_colType)

        if cur_dic_table_pref['colType']:
            self.combo_box_colType.setCurrentIndex(
                list_of_coltypes_in_comboBox.index(
                    list(filter(lambda x: list_of_types_dict_to_comboBox[x] == cur_dic_table_pref['colType'],
                                list_of_types_dict_to_comboBox))[0]))


class ColumnNameRow(QtWidgets.QTreeWidgetItem):
    iterator = 0
    def __init__(self, column_property, parent, tree_widget, columns_names_source, after_widget=None, adapter=None):
        super().__init__(parent, after_widget)
        self.label = QtWidgets.QLabel(adapter.take_translate('SourceColumnsConfigEditor', 'colName'))
        list_combo_box_dictTableName = columns_names_source
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItems(list_combo_box_dictTableName)
        self.objectName = 'colName'
        self.unique_name = f"{ColumnNameRow}_{ColumnNameRow.iterator}"
        ColumnNameRow.iterator = ColumnNameRow.iterator + 1
        if column_property['colName']:
            self.combo_box.setCurrentIndex(list_combo_box_dictTableName.index(column_property['colName']))
        else:
            self.combo_box.addItem('---')
            self.combo_box.setCurrentText('---')
        self.column_property = column_property
        tree_widget.setItemWidget(self, 1, self.combo_box)
        tree_widget.setItemWidget(self, 0, self.label)


class ColumnNameDbRow(QtWidgets.QTreeWidgetItem):
    def __init__(self,
                 column_property,
                 parent,
                 tree_widget,
                 columns_in_receiver,
                 adapter,
                 table_name,
                 validator,
                 dbtype,
                 db_base,
                 connector,
                 executor,
                 cur,
                 loggerInst
                 ):
        super().__init__(parent, [adapter.take_translate('SourceColumnsConfigEditor', 'colNameDb'), ])

        self.combo_box_colnameDb = QtWidgets.QComboBox()
        self.validator = validator
        self.dbtype = dbtype
        self.dbBase = db_base
        self.connector = connector
        self.executor = executor
        self.cur = cur
        self.loggerInst = loggerInst
        self.table_name=table_name
        if columns_in_receiver:
            list_colname_in_db_dict = [i[0] for i in columns_in_receiver]
            self.combo_box_colnameDb.addItems(list_colname_in_db_dict)

        if column_property['colNameDb']:
            self.combo_box_colnameDb.setCurrentIndex(list_colname_in_db_dict.index(column_property['colNameDb']))
        else:
            self.combo_box_colnameDb.addItem('---')
            self.combo_box_colnameDb.setCurrentText('---')
        tree_widget.setItemWidget(self, 1, self.combo_box_colnameDb)

        self.table_name.currentTextChanged.connect(self.cur_table_change)

    def cur_table_change(self, name):
        if not isinstance(self.validator, type):
            col_names_in_db_dict = self.validator.queryForColumnsInDict(f'{name}')
        else:
            col_names_in_db_dict = self.validator.queryForColumnsInDict_edit(
                dict_table_name=f"{name}",
                dbtype=self.dbtype,
                dbBase=self.dbBase,
                connector=self.connector,
                exec=self.executor,
                cur=self.cur,
                loggerInst=self.loggerInst
            )

        list_indxColumnDic = [i[0] for i in col_names_in_db_dict]

        while self.combo_box_colnameDb.count() > 0:
            self.combo_box_colnameDb.removeItem(0)
        self.combo_box_colnameDb.addItems(list_indxColumnDic)


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
        if self.column_property['cropEnd_mode']:
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
        if self.column_property['addValueEnd_mode']:
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
        if self.column_property['takeFromBegin_mode'] :
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
        if self.column_property['cropBegin_mode']:
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
        if self.column_property['addValueBegin_mode'] :
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
        if self.column_property['addValueBoth_mode']:
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
    def __init__(
            self,
            column_property: dict,
            parent: QtWidgets.QTreeWidget,
            parent_widget,
            after_widget=None,
            row: dict=None,
            table_item=None,
            adapter=None
    ):
        super().__init__(parent_widget, after_widget)
        self.column_property = column_property
        self.table_item = table_item
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
        if self.column_property['replace_mode']:
            if self.row:
                if self.column_property['replace_mode'] != 'false':
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
