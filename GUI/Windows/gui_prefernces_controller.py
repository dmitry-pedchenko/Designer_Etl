from PyQt5 import QtWidgets, QtCore
from GUI.gui_qt import form_preferences
import os
from PyQt5 import QtGui
import pandas as pd
from GUI.Windows.alarm_window import show_alarm_window


class Pref_Window(QtWidgets.QWidget):
    def __init__(self,
                 main_gui_widget,
                 config_dict: dict,
                 pref: dict,
                 logger_inst,
                 tables_in_db,
                 schemas_in_db,
                 dbService=None,
                 parent=None,
                 adapter=None):
        super().__init__()
        self.parent = parent
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.dbService = dbService
        if dbService:
            self.df = dbService.df
        self.df_compare = None
        self.schemas_in_db = schemas_in_db
        self.tables_in_db = tables_in_db
        self.logger_inst = logger_inst
        self.main_gui = main_gui_widget
        self.config_dict = config_dict
        self.ui = form_preferences.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_dbtype.setText(adapter.take_translate('pref_window', 'dbtype'))
        self.ui.label_dbHost.setText(adapter.take_translate('pref_window', 'dbHost'))
        self.ui.label_dbUser.setText(adapter.take_translate('pref_window', 'dbUser'))
        self.ui.label_dbPass.setText(adapter.take_translate('pref_window', 'dbPass'))
        self.ui.label_dbBase.setText(adapter.take_translate('pref_window', 'dbBase'))
        self.ui.label_dbScheme.setText(adapter.take_translate('pref_window', 'dbScheme'))
        self.ui.label_dbPort.setText(adapter.take_translate('pref_window', 'dbPort'))
        self.ui.label_loadMode.setText(adapter.take_translate('pref_window', 'Load_Mode'))
        self.ui.checkBox_Dictionary.setText(adapter.take_translate('pref_window', 'Dictionary'))
        self.ui.label_source.setText(adapter.take_translate('pref_window', 'Source_excel_file_name'))
        self.ui.label_receiver.setText(adapter.take_translate('pref_window', 'Target_table_name'))
        self.ui.checkBox_checkMode.setText(adapter.take_translate('pref_window', 'Check_mode'))
        self.ui.label_check_mode.setText(adapter.take_translate('pref_window', 'Check_table_name'))
        self.ui.checkBox_both.setText(adapter.take_translate('pref_window', 'Both'))

        self.treeWidget_linked_columns = TreeWidgetLinkedColumns(widget_sighal=self.ui.excelFileName)
        self.ui.tree_widget_box.addWidget(self.treeWidget_linked_columns)
        self.treeWidget_linked_columns.setHeaderLabels([adapter.take_translate('pref_window', 'LinkedColumnsCOLUMN'),
                                                        adapter.take_translate('pref_window', 'TargetColumnsCOLUMN')])
        self.treeWidget_linked_columns.setColumnCount(2)

        self.comboBox_list_source_excel = comboBox_list_source_excel(
            self.ui.horizontalLayoutWidget_3,
            check_widget=self.treeWidget_linked_columns
        )

        self.comboBox_list_source_excel.setObjectName("comboBox_list_source_excel")
        self.ui.horizontalLayout_3.addWidget(self.comboBox_list_source_excel)
        self.comboBox_list_source_excel.installEventFilter(ev_filt(parent=self.comboBox_list_source_excel))

        self.comboBox_set_list_checked = comboBox_list_source_excel(
            self.ui.horizontalLayoutWidget_5,
            check_widget=self.treeWidget_linked_columns
        )

        self.comboBox_set_list_checked.setObjectName("comboBox_set_list_checked")
        self.ui.horizontalLayout_5.addWidget(self.comboBox_set_list_checked)
        self.comboBox_set_list_checked.installEventFilter(ev_filt(parent=self.comboBox_set_list_checked))

        self.ui.comboBox_chose_loadMode.insertItem(0, 'insert')
        self.ui.comboBox_chose_loadMode.insertItem(1, 'update')
        list_of_db_types = ['mysql', 'mssql']
        self.ui.lineEdit_dbtype.addItems(list_of_db_types)
        self.pref = pref
        self.pref['col_to_check'] = []
        if config_dict:
            self.initialize()

        self.ui.button_save_pref.clicked.connect(self.save_db_pref)

        self.ui.lineEdit_dbtype.currentIndexChanged.connect(self.add_asterisc_dbtype)
        self.ui.lineEdit_dbhost.textChanged.connect(self.add_asterisc_dbhost)
        self.ui.lineEdit_dbuser.textChanged.connect(self.add_asterisc_dbuser)
        self.ui.lineEdit_dbpass.textChanged.connect(self.add_asterisc_dbpass)
        self.ui.lineEdit_dbbase.textChanged.connect(self.add_asterisc_dbbase)
        self.ui.lineEdit_dbport.textChanged.connect(self.add_asterisc_dbport)
        self.ui.excelFileName.textChanged.connect(self.add_asterisc_label_receiver)
        self.comboBox_list_source_excel.currentIndexChanged.connect(self.add_asterisc_label_receiver)

        self.ui.compare_file.textChanged.connect(self.add_asterisc_checkMode)
        self.comboBox_set_list_checked.currentIndexChanged.connect(self.add_asterisc_checkMode)

        self.ui.checkBox_checkMode.stateChanged.connect(self.add_asterisc_checkBox_checkMode)
        self.ui.checkBox_Dictionary.stateChanged.connect(self.add_asterisc_checkBox_Dictionary)
        self.ui.comboBox_chose_loadMode.currentIndexChanged.connect(self.add_asterisc_loadMode)
        self.ui.open_excel_file.clicked.connect(self.open_excel_folder)
        self.treeWidget_linked_columns.actionAddColumn.triggered.connect(self.add_link_col)
        self.treeWidget_linked_columns.actionDeleteColumn.triggered.connect(self.delete_link_col)
        self.ui.open_excel_compare_file.clicked.connect(self.open_excel_compare_folder)

    def open_excel_compare_folder(self):

        path_name = QtWidgets.QFileDialog.getOpenFileName(directory=os.path.join(os.getcwd(), 'Source'),
                                                          filter='*.xlsx')
        path = os.path.basename(path_name[0])

        if path:

            if self.treeWidget_linked_columns.topLevelItemCount() > 0:
                result = QtWidgets.QMessageBox.question(self,
                                                                "Change file ?",
                                                                "Change file ? Linked columns will remove",
                                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                                QtWidgets.QMessageBox.No
                                                                )

                if result == QtWidgets.QMessageBox.Yes:
                    self.ui.compare_file.setText(path)
                    pathToExcel = os.path.join(os.path.join(os.getcwd(), 'Source'),
                                               path)
                    self.df_compare = pd.ExcelFile(pathToExcel)
                    self.comboBox_set_list_checked.clear()
                    self.comboBox_set_list_checked.addItems([i for i in self.df_compare.sheet_names])
                    self.ui.compare_file.textChanged.emit(path)
                    self.comboBox_set_list_checked.currentIndexChanged.emit(0)
            else:
                self.ui.compare_file.setText(path)
                pathToExcel = os.path.join(os.path.join(os.getcwd(), 'Source'),
                                           path)
                self.df_compare = pd.ExcelFile(pathToExcel)
                self.comboBox_set_list_checked.clear()
                self.comboBox_set_list_checked.addItems([i for i in self.df_compare.sheet_names])
                self.ui.compare_file.textChanged.emit(path)
                self.comboBox_set_list_checked.currentIndexChanged.emit(0)

    def add_link_col(self):
        if self.df_compare:
            target_column = [i for i in self.df_compare.parse(self.comboBox_set_list_checked.currentIndex()).columns.values]
        else:
            show_alarm_window(self, "Choose a file !!!")
            return

        source_column = [i for i in self.df.parse(self.comboBox_list_source_excel.currentIndex()).columns.values]

        row_check = LinkedColumns(
            tree_widget=self.treeWidget_linked_columns,
            parent=self.treeWidget_linked_columns,
            target_columns=target_column,
            source_columns=source_column,
            current_column=None)
        self.treeWidget_linked_columns.addTopLevelItem(row_check)

        self.pref['col_to_check'].append(row_check)

    def delete_link_col(self):
        self.pref['col_to_check'].remove(self.treeWidget_linked_columns.currentItem())
        self.treeWidget_linked_columns.takeTopLevelItem(
            self.treeWidget_linked_columns.indexFromItem(self.treeWidget_linked_columns.currentItem()).row())

    def create_links_columns(self):

        path = self.config_dict["pathToLinkFile"]
        self.ui.compare_file.setText(path)
        pathToExcel = os.path.join(os.path.join(os.getcwd(), 'Source'),
                                   path)
        df_temp = pd.ExcelFile(pathToExcel)
        self.df_compare = None
        self.df_compare = df_temp.parse(self.config_dict['linkedFileSheetNumber'])

        if self.df_compare is not None:
            target_column = [i for i in self.df_compare.columns.values]
        else:
            target_column = None

        self.comboBox_set_list_checked.clear()
        self.comboBox_set_list_checked.addItems([i for i in df_temp.sheet_names])
        self.comboBox_set_list_checked.setCurrentIndex(self.config_dict['linkedFileSheetNumber'])
        if self.dbService:
            source_column = [i for i in self.dbService.dataFrame.columns.values]
        else:
            source_column = None

        arr_of_col = []
        for row in self.config_dict['linkedColumns']:
            row_check = LinkedColumns(
                                      tree_widget=self.treeWidget_linked_columns,
                                      parent=self.treeWidget_linked_columns,
                                      target_columns=target_column,
                                      source_columns=source_column,
                                      current_column=row)

            arr_of_col.append(row_check)
            self.treeWidget_linked_columns.addTopLevelItem(row_check)
        self.pref['col_to_check'] = arr_of_col

    def initialize(self):
        self.ui.lineEdit_dbtype.setCurrentText(self.config_dict['dbtype'])
        self.ui.lineEdit_dbport.setText(self.config_dict['dbPort'])
        self.ui.lineEdit_dbbase.setText(self.config_dict['dbBase'])
        self.ui.lineEdit_dbpass.setText(self.config_dict['dbPass'])
        self.ui.lineEdit_dbuser.setText(self.config_dict['dbUser'])
        self.ui.lineEdit_dbhost.setText(self.config_dict['dbHost'])
        self.ui.excelFileName.setText(self.config_dict['importXml_path_value'])
        self.ui.comboBox_chose_loadMode.setCurrentText(self.config_dict['loadMode'])
        self.ui.target_table_name.addItems(sorted(self.tables_in_db))
        self.ui.target_table_name.setCurrentIndex(sorted(self.tables_in_db).index(self.config_dict['exportTableName_value_text']))

        if self.config_dict['checkMode_value'] == 'true':

            self.ui.comboBox_dbSchema.addItems(self.schemas_in_db)
            self.ui.comboBox_dbSchema.setCurrentIndex(self.schemas_in_db.index(self.config_dict['db_schema']))

            self.ui.checkBox_Dictionary.setCheckState(QtCore.Qt.Unchecked)
            self.ui.checkBox_Dictionary.setDisabled(True)

            self.ui.checkBox_checkMode.setCheckState(QtCore.Qt.Checked)
            self.create_links_columns()

            pathToExcel = os.path.join(os.path.join(os.getcwd(), 'Source'),
                                       self.config_dict['pathToLinkFile'])
            self.df_compare = pd.ExcelFile(pathToExcel)

            self.ui.compare_file.setText(self.config_dict['pathToLinkFile'])
            self.comboBox_list_source_excel.addItems([i for i in self.dbService.df.sheet_names])
            self.comboBox_list_source_excel.setCurrentIndex(int(self.config_dict['linkedFileSheetNumber']))
            if self.config_dict['if_both'] == 'true':
                self.ui.checkBox_both.setCheckState(QtCore.Qt.Checked)

        else:
            self.ui.checkBox_checkMode.setCheckState(QtCore.Qt.Unchecked)
            self.ui.label_check_mode.setDisabled(True)
            self.ui.open_excel_compare_file.setDisabled(True)
            self.ui.compare_file.setDisabled(True)
            self.comboBox_set_list_checked.setDisabled(True)
            self.treeWidget_linked_columns.setDisabled(True)
            self.ui.checkBox_both.setDisabled(True)

        if self.config_dict['dictMode'] == 'true':
            self.ui.checkBox_Dictionary.setCheckState(QtCore.Qt.Checked)
        else:
            self.ui.checkBox_Dictionary.setCheckState(QtCore.Qt.Unchecked)

        self.comboBox_list_source_excel.addItems([i for i in self.dbService.df.sheet_names])
        self.comboBox_list_source_excel.setCurrentIndex(int(self.config_dict['sheetNumber_value']))

        if self.config_dict['checkMode_value'] == 'false':
            self.ui.comboBox_dbSchema.addItems(self.schemas_in_db)
            self.ui.comboBox_dbSchema.setCurrentIndex(self.schemas_in_db.index(self.config_dict['db_schema']))

        self.pref['dbtype'] = self.ui.lineEdit_dbtype.currentText()
        self.pref['dbHost'] = self.ui.lineEdit_dbhost.text()
        self.pref['dbUser'] = self.ui.lineEdit_dbuser.text()
        self.pref['dbPass'] = self.ui.lineEdit_dbpass.text()
        self.pref['dbBase'] = self.ui.lineEdit_dbbase.text()
        self.pref['dbPort'] = self.ui.lineEdit_dbport.text()
        self.pref['dbSchema'] = self.ui.comboBox_dbSchema.currentText()
        self.pref['Load Mode'] = self.ui.comboBox_chose_loadMode.currentText()
        self.pref['excelFileName'] = self.ui.excelFileName.text()
        self.pref['comboBox_list_source_excel'] = self.comboBox_list_source_excel.currentIndex()
        self.pref['target_table_name'] = self.ui.target_table_name.currentText()
        self.pref['checkBox_checkMode'] = self.ui.checkBox_checkMode.isChecked()
        self.pref['compare_file'] = self.ui.compare_file.text()
        self.pref['comboBox_set_list_checked'] = self.comboBox_set_list_checked.currentText()
        self.pref['checkBox_Dictionary'] = self.ui.checkBox_Dictionary.isChecked()
        self.pref['checkBox_both'] = self.ui.checkBox_both.isChecked()

        self.ui.lineEdit_dbtype.setDisabled(True)
        self.ui.comboBox_dbSchema.setDisabled(True)
        self.ui.target_table_name.setDisabled(True)

    def add_asterisc_checkBox_Dictionary(self):
        if self.ui.checkBox_Dictionary.text()[0] != '*':
            self.ui.checkBox_Dictionary.setText(f"*{self.ui.checkBox_Dictionary.text()}")
            self.ui.checkBox_Dictionary.adjustSize()

    def add_asterisc_dbtype(self):
        if self.ui.label_dbtype.text()[0] != '*':
            self.ui.label_dbtype.setText(f"*{self.ui.label_dbtype.text()}")
            self.ui.label_dbtype.adjustSize()

    def add_asterisc_checkMode(self):

        while self.treeWidget_linked_columns.topLevelItemCount() > 0:
            self.treeWidget_linked_columns.takeTopLevelItem(0)


        if self.ui.checkBox_checkMode.text()[0] != '*':
            self.ui.checkBox_checkMode.setText(f"*{self.ui.checkBox_checkMode.text()}")
            self.ui.checkBox_checkMode.adjustSize()

    def add_asterisc_dbhost(self):
        if self.ui.label_dbHost.text()[0] != '*':
            self.ui.label_dbHost.setText(f"*{self.ui.label_dbHost.text()}")
            self.ui.label_dbHost.adjustSize()

    def add_asterisc_dbuser(self):
        if self.ui.label_dbUser.text()[0] != '*':
            self.ui.label_dbUser.setText(f"*{self.ui.label_dbUser.text()}")
            self.ui.label_dbUser.adjustSize()

    def add_asterisc_dbpass(self):
        if self.ui.label_dbPass.text()[0] != '*':
            self.ui.label_dbPass.setText(f"*{self.ui.label_dbPass.text()}")
            self.ui.label_dbPass.adjustSize()

    def add_asterisc_dbbase(self):
        if self.ui.label_dbBase.text()[0] != '*':
            self.ui.label_dbBase.setText(f"*{self.ui.label_dbBase.text()}")
            self.ui.label_dbBase.adjustSize()

    def add_asterisc_dbport(self):
        if self.ui.label_dbPort.text()[0] != '*':
            self.ui.label_dbPort.setText(f"*{self.ui.label_dbPort.text()}")
            self.ui.label_dbPort.adjustSize()

    def add_asterisc_checkBox_checkMode(self):
        if self.ui.checkBox_checkMode.isChecked():
            self.ui.label_check_mode.setDisabled(True)
            self.ui.label_check_mode.setDisabled(False)
            self.ui.open_excel_compare_file.setDisabled(False)
            self.ui.compare_file.setDisabled(False)
            self.comboBox_set_list_checked.setDisabled(False)
            self.ui.checkBox_Dictionary.setDisabled(True)
            self.ui.checkBox_Dictionary.setChecked(False)
            self.treeWidget_linked_columns.setDisabled(False)
            self.ui.checkBox_both.setDisabled(False)

        else:
            self.ui.label_check_mode.setDisabled(False)
            self.ui.label_check_mode.setDisabled(True)
            self.ui.open_excel_compare_file.setDisabled(True)
            self.ui.compare_file.setDisabled(True)
            self.comboBox_set_list_checked.setDisabled(True)
            self.ui.checkBox_Dictionary.setDisabled(False)
            self.treeWidget_linked_columns.setDisabled(True)
            self.ui.checkBox_both.setDisabled(True)

        if self.ui.checkBox_checkMode.text()[0] != '*':
            self.ui.checkBox_checkMode.setText(f"*{self.ui.checkBox_checkMode.text()}")
            self.ui.checkBox_checkMode.adjustSize()

    def add_asterisc_loadMode(self):
        if self.ui.label_loadMode.text()[0] != '*':
            self.ui.label_loadMode.setText(f"*{self.ui.label_loadMode.text()}")
            self.ui.label_loadMode.adjustSize()

    def add_asterisc_label_receiver(self):
        while self.treeWidget_linked_columns.topLevelItemCount() > 0:
            self.treeWidget_linked_columns.takeTopLevelItem(0)

        if self.ui.label_source.text()[0] != '*':
            self.ui.label_source.setText(f"*{self.ui.label_source.text()}")
            self.ui.label_source.adjustSize()

    def save_db_pref(self):
        if self.ui.label_dbtype.text()[0] == '*':
            self.ui.label_dbtype.setText(f"{self.ui.label_dbtype.text()[1:]}")
            self.ui.label_dbtype.adjustSize()
        if self.ui.label_dbHost.text()[0] == '*':
            self.ui.label_dbHost.setText(f"{self.ui.label_dbHost.text()[1:]}")
            self.ui.label_dbHost.adjustSize()
        if self.ui.label_dbUser.text()[0] == '*':
            self.ui.label_dbUser.setText(f"{self.ui.label_dbUser.text()[1:]}")
            self.ui.label_dbUser.adjustSize()
        if self.ui.label_dbPass.text()[0] == '*':
            self.ui.label_dbPass.setText(f"{self.ui.label_dbPass.text()[1:]}")
            self.ui.label_dbPass.adjustSize()
        if self.ui.label_dbBase.text()[0] == '*':
            self.ui.label_dbBase.setText(f"{self.ui.label_dbBase.text()[1:]}")
            self.ui.label_dbBase.adjustSize()
        if self.ui.label_dbPort.text()[0] == '*':
            self.ui.label_dbPort.setText(f"{self.ui.label_dbPort.text()[1:]}")
            self.ui.label_dbPort.adjustSize()

        if self.ui.checkBox_checkMode.text()[0] == '*':
            self.ui.checkBox_checkMode.setText(f"{self.ui.checkBox_checkMode.text()[1:]}")
            self.ui.checkBox_checkMode.adjustSize()

        if self.ui.checkBox_Dictionary.text()[0] == '*':
            self.ui.checkBox_Dictionary.setText(f"{self.ui.checkBox_Dictionary.text()[1:]}")
            self.ui.checkBox_Dictionary.adjustSize()

        if self.ui.label_loadMode.text()[0] == '*':
            self.ui.label_loadMode.setText(f"{self.ui.label_loadMode.text()[1:]}")
            self.ui.label_loadMode.adjustSize()

        if self.ui.label_source.text()[0] == '*':
            self.ui.label_source.setText(f"{self.ui.label_source.text()[1:]}")
            self.ui.label_source.adjustSize()

        if self.ui.checkBox_Dictionary.isChecked():
            self.main_gui.ui.actionDictionary.setChecked(True)
            self.main_gui.ui.actionDictionary.triggered.emit(1)
        else:
            self.main_gui.ui.actionDictionary.setChecked(False)
            self.main_gui.ui.actionDictionary.triggered.emit(0)


        self.pref['dbtype'] = self.ui.lineEdit_dbtype.currentText()
        self.pref['dbHost'] = self.ui.lineEdit_dbhost.text()
        self.pref['dbUser'] = self.ui.lineEdit_dbuser.text()
        self.pref['dbPass'] = self.ui.lineEdit_dbpass.text()
        self.pref['dbBase'] = self.ui.lineEdit_dbbase.text()
        self.pref['dbPort'] = self.ui.lineEdit_dbport.text()
        self.pref['dbSchema'] = self.ui.comboBox_dbSchema.currentText()
        self.pref['Load Mode'] = self.ui.comboBox_chose_loadMode.currentText()
        self.pref['excelFileName'] = self.ui.excelFileName.text()
        self.pref['comboBox_list_source_excel'] = self.comboBox_list_source_excel.currentIndex()
        self.pref['target_table_name'] = self.ui.target_table_name.currentText()
        self.pref['checkBox_checkMode'] = self.ui.checkBox_checkMode.isChecked()
        self.pref['compare_file'] = self.ui.compare_file.text()
        self.pref['comboBox_set_list_checked'] = self.comboBox_set_list_checked.currentText()
        self.pref['checkBox_Dictionary'] = self.ui.checkBox_Dictionary.isChecked()
        self.pref['checkBox_both'] = f'{self.ui.checkBox_both.isChecked()}'.lower()

    def open_excel_folder(self):

        path_name = QtWidgets.QFileDialog.getOpenFileName(directory=os.path.join(os.getcwd(), 'Source'),
                                                          filter='*.xlsx')
        path = os.path.basename(path_name[0])
        if path:

            if self.treeWidget_linked_columns.topLevelItemCount() > 0:
                result = QtWidgets.QMessageBox.question(self,
                                                        "Change file ?",
                                                        "Change file ? Linked columns will remove",
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                        QtWidgets.QMessageBox.No
                                                        )

                if result == QtWidgets.QMessageBox.Yes:
                    self.ui.excelFileName.setText(path)
                    pathToExcel = os.path.join(os.path.join(os.getcwd(), 'Source'), path)
                    self.df = pd.ExcelFile(pathToExcel)
                    self.comboBox_list_source_excel.clear()
                    self.comboBox_list_source_excel.addItems([i for i in self.df.sheet_names])
                    self.ui.excelFileName.textChanged.emit(path)
                    self.comboBox_list_source_excel.currentIndexChanged.emit(0)
            else:
                self.ui.excelFileName.setText(path)
                pathToExcel = os.path.join(os.path.join(os.getcwd(), 'Source'), path)
                self.df = pd.ExcelFile(pathToExcel)
                self.comboBox_list_source_excel.clear()
                self.comboBox_list_source_excel.addItems([i for i in self.df.sheet_names])
                self.ui.excelFileName.textChanged.emit(path)
                self.comboBox_list_source_excel.currentIndexChanged.emit(0)


class LinkedColumns(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, current_column, parent, target_columns, source_columns):
        super().__init__(parent, ['', ])

        self.combo_box_source_links = QtWidgets.QComboBox()
        self.combo_box_target_links = QtWidgets.QComboBox()

        self.combo_box_source_links.addItems(source_columns)
        self.combo_box_target_links.addItems(target_columns)

        if current_column: # если есть колонка из которой создается
            self.combo_box_source_links.setCurrentIndex(source_columns.index(current_column['colNameInSource']))
            self.combo_box_target_links.setCurrentIndex(target_columns.index(current_column['linkedColName']))

        tree_widget.setItemWidget(self, 0, self.combo_box_source_links)
        tree_widget.setItemWidget(self, 1, self.combo_box_target_links)


class TreeWidgetLinkedColumns(QtWidgets.QTreeWidget):
    def __init__(self, parent=None, widget_sighal=None):
        super().__init__(parent)

        self.widget_sighal = widget_sighal
        self.treeWidget_linked_columns = QtWidgets.QTreeWidget()
        self.treeWidget_linked_columns.setGeometry(QtCore.QRect(10, 260, 271, 101))
        self.treeWidget_linked_columns.setObjectName("treeWidget_linked_columns")
        self.treeWidget_linked_columns.headerItem().setText(0, "1")

        self.context_menu_add_row = QtWidgets.QMenu()
        self.actionAddColumn = QtWidgets.QAction()
        self.actionDeleteColumn = QtWidgets.QAction()
        self.actionAddColumn.setText("Add Column")
        self.actionDeleteColumn.setText("Delete Column")
        self.context_menu_add_row.addAction(self.actionAddColumn)
        self.context_menu_add_row.addAction(self.actionDeleteColumn)
        self.widget_sighal.textChanged.connect(self.delete_columns)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent) -> None:
        self.context_menu_add_row.exec(event.globalPos())

    def delete_columns(self):
        while self.topLevelItemCount() > 0:
            self.takeTopLevelItem(0)


class comboBox_list_source_excel(QtWidgets.QComboBox):
    def __init__(self, parent=None, check_widget=None):
        super().__init__(parent)
        self.check_widget = check_widget


class ev_filt(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, a0, a1) -> bool:
        if a1.type() == QtCore.QEvent.MouseButtonPress:
            if self.parent().check_widget.topLevelItemCount() > 0:
                result = QtWidgets.QMessageBox.question(None,
                                                        "Change list ?",
                                                        "Change list ? Linked columns will remove",
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                        QtWidgets.QMessageBox.No
                                                        )

                if result == QtWidgets.QMessageBox.No:
                    return True
                elif result == QtWidgets.QMessageBox.Yes:
                    return False
            else:
                return False
        else:
            return QtCore.QObject.eventFilter(self, a0, a1)






