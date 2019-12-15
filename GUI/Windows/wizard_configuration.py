from PyQt5 import QtCore, QtWidgets, QtGui
import GUI.gui_qt.form_wizard_page_1 as form_wizard_page_1
import GUI.gui_qt.form_wizard_page_2 as form_wizard_page_2
import GUI.gui_qt.form_wizard_page_3 as form_wizard_page_3
import GUI.gui_qt.form_wizard_page_4 as form_wizard_page_4
import GUI.gui_qt.form_wizard_page_5 as form_wizard_page_5
import GUI.gui_qt.form_wizard_page_6 as form_wizard_page_6
from GUI.Trees import Receiver_tree, Dict_tree, Source_tree
import xml.dom.minidom as xml_format
import os
import pandas as pd
import Core.DAO.DB_connector as db_con
from Core.Logger import Logger
from Core.Validate import Validate_res
from GUI.Windows.alarm_window import show_alarm_window
from GUI.Creators import source_column_editor_viewer, target_column_editor_viewer
import copy
from GUI.DAO.create_xml import CreateXML
import xml.etree.ElementTree as et


class WizardConfig(QtWidgets.QWizard):
    def __init__(self, parent, adapter):
        super().__init__(parent=parent)

        self.setPage(RoadMapConfiguration.db_parameters_and_check_mode, Page1(self, adapter=adapter))
        self.setPage(RoadMapConfiguration.target_table_and_db_schema, Page2(self, adapter=adapter))
        self.setPage(RoadMapConfiguration.source_columns, Page3(self, adapter=adapter))
        self.setPage(RoadMapConfiguration.receiver_columns, Page4(self, adapter=adapter))
        self.setPage(RoadMapConfiguration.dictionary, Page5(self, adapter=adapter))
        self.setPage(RoadMapConfiguration.final_page, Page6(self, adapter=adapter))

        self.resize(900, 700)

    def closeEvent(self, e):
        answer = QtWidgets.QMessageBox.question(self,
                                                "Question",
                                                "Exit from creator ?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.Yes
                                                )

        if answer == QtWidgets.QMessageBox.Yes:
            e.accept()
            QtWidgets.QWidget.closeEvent(self, e)
        else:
            e.ignore()


class Page1(QtWidgets.QWizardPage, form_wizard_page_1.Ui_Form):
    def __init__(self, parent=None, adapter=None):
        super().__init__(parent)
        self.loggerInst = Logger.Log_info.getInstance(pathToConfigXML='GUI', configs_list=['GUI'])

        self.pref = {'col_to_check': []}
        self.setupUi(self)
        self.adapter=adapter
        self.label_dbtype.setText(adapter.take_translate('pref_window', 'dbtype'))
        self.label_dbHost.setText(adapter.take_translate('pref_window', 'dbHost'))
        self.label_dbUser.setText(adapter.take_translate('pref_window', 'dbUser'))
        self.label_dbPass.setText(adapter.take_translate('pref_window', 'dbPass'))
        self.label_dbBase.setText(adapter.take_translate('pref_window', 'dbBase'))
        self.label_dbPort.setText(adapter.take_translate('pref_window', 'dbPort'))
        self.label_loadMode.setText(adapter.take_translate('pref_window', 'Load_Mode'))
        self.checkBox_Dictionary.setText(adapter.take_translate('pref_window', 'Dictionary'))
        self.label_source.setText(adapter.take_translate('pref_window', 'Source_excel_file_name'))
        self.checkBox_checkMode.setText(adapter.take_translate('pref_window', 'Check_mode'))
        self.label_check_mode.setText(adapter.take_translate('pref_window', 'Check_table_name'))
        self.checkBox_both.setText(adapter.take_translate('pref_window', 'Both'))

        self.change_flag = False
        self.open_excel_file = QtWidgets.QToolButton(self.horizontalLayoutWidget_3)
        self.open_excel_file.setObjectName("open_excel_file")
        self.horizontalLayout_3.insertWidget(0, self.open_excel_file)
        self.open_excel_file.setText("...")

        self.registerField('dictionary_state', self.checkBox_Dictionary)

        self.df_compare = None

        self.lineEdit_dbtype.addItems(['mysql', 'mssql'])
        self.comboBox_chose_loadMode.addItems(['insert', 'update'])

        self.treeWidget_linked_columns = TreeWidgetLinkedColumns(widget_sighal=self.excelFileName, pref_dict=self.pref, adapter=self.adapter)
        self.tree_widget_box.addWidget(self.treeWidget_linked_columns)
        self.treeWidget_linked_columns.setHeaderLabels([adapter.take_translate('pref_window', 'LinkedColumnsCOLUMN'),
                                                        adapter.take_translate('pref_window', 'TargetColumnsCOLUMN')])
        self.treeWidget_linked_columns.setColumnCount(2)

        self.comboBox_list_source_excel = comboBox_list_for_Page2(
            self.horizontalLayoutWidget_3,
            check_widget=self.treeWidget_linked_columns
        )

        self.comboBox_list_source_excel.setObjectName("comboBox_list_source_excel")
        self.horizontalLayout_3.addWidget(self.comboBox_list_source_excel)
        self.comboBox_list_source_excel.installEventFilter(ev_filt(parent=self.comboBox_list_source_excel))

        self.comboBox_set_list_checked = comboBox_list_for_Page2(
            self.horizontalLayoutWidget_5,
            check_widget=self.treeWidget_linked_columns
        )

        self.comboBox_set_list_checked.setObjectName("comboBox_set_list_checked")
        self.horizontalLayout_5.addWidget(self.comboBox_set_list_checked)
        self.comboBox_set_list_checked.installEventFilter(ev_filt(parent=self.comboBox_set_list_checked))

        self.label_check_mode.setDisabled(False)
        self.label_check_mode.setDisabled(True)
        self.open_excel_compare_file.setDisabled(True)
        self.compare_file.setDisabled(True)
        self.comboBox_set_list_checked.setDisabled(True)
        self.checkBox_Dictionary.setDisabled(False)
        self.treeWidget_linked_columns.setDisabled(True)
        self.checkBox_both.setDisabled(True)
        self.compare_file.setDisabled(True)

        self.open_excel_file.clicked.connect(self.open_excel_folder)
        self.open_excel_compare_file.clicked.connect(self.open_excel_compare_folder)
        self.checkBox_checkMode.stateChanged.connect(self.add_asterisc_checkBox_checkMode)

        self.treeWidget_linked_columns.actionAddColumn.triggered.connect(self.add_link_col)
        self.treeWidget_linked_columns.actionDeleteColumn.triggered.connect(self.delete_link_col)
        self.comboBox_list_source_excel.currentIndexChanged.connect(self.add_asterisc_label_receiver)
        self.comboBox_set_list_checked.currentIndexChanged.connect(self.add_asterisc_checkMode)
        self.excelFileName.textChanged.connect(self.add_asterisc_label_receiver)
        self.compare_file.textChanged.connect(self.add_asterisc_checkMode)

        self.lineEdit_dbhost.textEdited.connect(self.set_flag)
        self.lineEdit_dbpass.textEdited.connect(self.set_flag)
        self.lineEdit_dbport.textEdited.connect(self.set_flag)
        self.lineEdit_dbuser.textEdited.connect(self.set_flag)
        self.lineEdit_dbbase.textEdited.connect(self.set_flag)

    def set_flag(self):
        self.change_flag = True

    def add_asterisc_checkMode(self):

        while self.treeWidget_linked_columns.topLevelItemCount() > 0:
            self.treeWidget_linked_columns.takeTopLevelItem(0)

    def add_asterisc_label_receiver(self):
        while self.treeWidget_linked_columns.topLevelItemCount() > 0:
            self.treeWidget_linked_columns.takeTopLevelItem(0)

    def add_asterisc_checkMode(self):

        while self.treeWidget_linked_columns.topLevelItemCount() > 0:
            self.treeWidget_linked_columns.takeTopLevelItem(0)

    def add_asterisc_label_receiver(self):
        while self.treeWidget_linked_columns.topLevelItemCount() > 0:
            self.treeWidget_linked_columns.takeTopLevelItem(0)

    def add_link_col(self):
        self.registerField('tree_widget_box_link_columns', self.treeWidget_linked_columns)

        if self.df_compare:
            target_column = [i for i in self.df_compare.parse(self.comboBox_set_list_checked.currentIndex()).columns.values]
        else:
            show_alarm_window(self, "Choose a link file !!!")
            return

        try:
            source_column = [i for i in self.df.parse(self.comboBox_list_source_excel.currentIndex()).columns.values]
        except:
            show_alarm_window(self, "Choose a source file !!!")
            return


        row_check = LinkedColumns(
            tree_widget=self.treeWidget_linked_columns,
            parent=self.treeWidget_linked_columns,
            target_columns=target_column,
            source_columns=source_column,
            current_column=None,
            adapter=self.adapter)
        self.treeWidget_linked_columns.addTopLevelItem(row_check)

        self.pref['col_to_check'].append(row_check)

    def delete_link_col(self):
        self.pref['col_to_check'].remove(self.treeWidget_linked_columns.currentItem())
        self.treeWidget_linked_columns.takeTopLevelItem(
            self.treeWidget_linked_columns.indexFromItem(self.treeWidget_linked_columns.currentItem()).row())

    def open_excel_folder(self):

        path_name = QtWidgets.QFileDialog.getOpenFileName(directory=os.path.join(os.getcwd(), 'Source'),
                                                          filter='*.xlsx')
        path = os.path.basename(path_name[0])
        if path:

            if self.treeWidget_linked_columns.topLevelItemCount() > 0 or \
                    self.wizard().page(2).treeWidget_of_Source.topLevelItemCount() > 0 or \
                    (hasattr(self.wizard().page(4), "tree_dict") and self.wizard().page(4).tree_dict.topLevelItemCount() > 0):
                result = QtWidgets.QMessageBox.question(self,
                                                        "Change file ?",
                                                        "Change file ? Linked columns and Source Columns will remove",
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                        QtWidgets.QMessageBox.No
                                                        )

                if result == QtWidgets.QMessageBox.Yes:
                    self.excelFileName.setText(path)
                    pathToExcel = os.path.join(os.path.join(os.getcwd(), 'Source'), path)
                    self.df = pd.ExcelFile(pathToExcel)
                    self.comboBox_list_source_excel.clear()
                    self.comboBox_list_source_excel.addItems([i for i in self.df.sheet_names])
                    self.excelFileName.textChanged.emit(path)
                    self.comboBox_list_source_excel.currentIndexChanged.emit(0)
            else:
                self.excelFileName.setText(path)
                pathToExcel = os.path.join(os.path.join(os.getcwd(), 'Source'), path)
                self.df = pd.ExcelFile(pathToExcel)
                self.comboBox_list_source_excel.clear()
                self.comboBox_list_source_excel.addItems([i for i in self.df.sheet_names])
                self.excelFileName.textChanged.emit(path)
                self.comboBox_list_source_excel.currentIndexChanged.emit(0)

    def open_excel_compare_folder(self):

        path_name_compare_excel = QtWidgets.QFileDialog.getOpenFileName(directory=os.path.join(os.getcwd(), 'Source'),
                                                          filter='*.xlsx')
        path_compare_excel = os.path.basename(path_name_compare_excel[0])

        if path_compare_excel:
            self.path_name_compare_excel = path_name_compare_excel[0]
            self.path_compare_excel = path_compare_excel

            if self.treeWidget_linked_columns.topLevelItemCount() > 0:
                result = QtWidgets.QMessageBox.question(self,
                                                                "Change file ?",
                                                                "Change file ? Linked columns will remove",
                                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                                QtWidgets.QMessageBox.No
                                                                )

                if result == QtWidgets.QMessageBox.Yes:
                    self.compare_file.setText(path_compare_excel)
                    pathToExcel = os.path.join(os.path.join(os.getcwd(), 'Source'),
                                               path_compare_excel)
                    self.df_compare = pd.ExcelFile(pathToExcel)
                    self.comboBox_set_list_checked.clear()
                    self.comboBox_set_list_checked.addItems([i for i in self.df_compare.sheet_names])
                    self.compare_file.textChanged.emit(path_compare_excel)
                    self.comboBox_set_list_checked.currentIndexChanged.emit(0)
            else:
                self.compare_file.setText(path_compare_excel)
                pathToExcel = os.path.join(os.path.join(os.getcwd(), 'Source'),
                                           path_compare_excel)
                self.df_compare = pd.ExcelFile(pathToExcel)
                self.comboBox_set_list_checked.clear()
                self.comboBox_set_list_checked.addItems([i for i in self.df_compare.sheet_names])
                self.compare_file.textChanged.emit(path_compare_excel)
                self.comboBox_set_list_checked.currentIndexChanged.emit(0)

    def add_asterisc_checkBox_checkMode(self):
        if self.checkBox_checkMode.isChecked():
            self.label_check_mode.setDisabled(True)
            self.label_check_mode.setDisabled(False)
            self.open_excel_compare_file.setDisabled(False)
            self.compare_file.setDisabled(False)
            self.comboBox_set_list_checked.setDisabled(False)
            self.checkBox_Dictionary.setDisabled(True)
            self.checkBox_Dictionary.setChecked(False)
            self.treeWidget_linked_columns.setDisabled(False)
            self.checkBox_both.setDisabled(False)
            self.compare_file.setDisabled(False)

        else:
            self.compare_file.setDisabled(True)
            self.label_check_mode.setDisabled(False)
            self.label_check_mode.setDisabled(True)
            self.open_excel_compare_file.setDisabled(True)
            self.compare_file.setDisabled(True)
            self.comboBox_set_list_checked.setDisabled(True)
            self.checkBox_Dictionary.setDisabled(False)
            self.treeWidget_linked_columns.setDisabled(True)
            self.checkBox_both.setDisabled(True)

    def validatePage(self) -> bool:
        if not self.excelFileName.text():
            show_alarm_window(self, "Choose a source file !!!")
            return False
        else:
            if self.change_flag is True or hasattr(self, "con") is False:
                if hasattr(self, "con"):
                    self.con.closeConnect()
                    del self.con
                self.wizard().page(1).comboBox_dbSchema.clear()
                self.wizard().page(1).target_table_name.clear()
                con = db_con.Connection.get_instance(self.loggerInst)
                try:
                    con.connectToTheDB(host=self.lineEdit_dbhost.text(),
                                       user=self.lineEdit_dbuser.text(),
                                       password=self.lineEdit_dbpass.text(),
                                       dbname=self.lineEdit_dbbase.text(),
                                       port=int(self.lineEdit_dbport.text()),
                                       dbtype=self.lineEdit_dbtype.currentText()
                                       )
                    con.test_conn(0)

                    self.pref['dbtype'] = self.lineEdit_dbtype.currentText()
                    self.pref['dbHost'] = self.lineEdit_dbhost.text()
                    self.pref['dbUser'] = self.lineEdit_dbuser.text()
                    self.pref['dbPass'] = self.lineEdit_dbpass.text()
                    self.pref['dbBase'] = self.lineEdit_dbbase.text()
                    self.pref['dbPort'] = self.lineEdit_dbport.text()

                    self.pref['Load Mode'] = self.comboBox_chose_loadMode.currentText()
                    self.pref['excelFileName'] = self.excelFileName.text()
                    self.pref['comboBox_list_source_excel'] = self.comboBox_list_source_excel.currentIndex()
                    self.pref['checkBox_checkMode'] = self.checkBox_checkMode.isChecked()
                    self.pref['compare_file'] = self.compare_file.text()
                    self.pref['comboBox_set_list_checked'] = self.comboBox_set_list_checked.currentText()
                    self.pref['checkBox_Dictionary'] = self.checkBox_Dictionary.isChecked()
                    self.pref['checkBox_both'] = self.checkBox_both.isChecked()

                except Exception:
                    if hasattr(self, "con"):
                        self.con.closeConnect()
                    show_alarm_window(self, "Can't connect to the DB !!!")
                    return False
                else:
                    self.change_flag = False
                    self.con = con
                    self.initializePage2()
                    return True
            else:
                try:
                    self.con.test_conn(0)
                except Exception:
                    if hasattr(self, "con"):
                        self.con.closeConnect()
                    show_alarm_window(self, "Can't connect to the DB !!!")
                    return False
                return True

    def close_project_data(self):
        self.pref = {}

    def initializePage2(self) -> None:

        self.wizard().page(1).comboBox_dbSchema.addItems(sorted([i[0] for i in Validate_res.Validate.queryForSchemasInDb_edit(
            dbtype=self.lineEdit_dbtype.currentText(),
            connector=self.con,
            executor=Validate_res.Validate.executor,
            cur=self.con.cursor,
            loggerInst=self.loggerInst
        )]))

        self.wizard().page(1).target_table_name.addItems(sorted([i[0] for i in Validate_res.Validate.queryForTableInDbList_edit(
            connector=self.con,
            dbtype=self.lineEdit_dbtype.currentText(),
            executor=Validate_res.Validate.executor,
            cur=self.con.cursor,
            loggerInst=self.loggerInst
        )]))



class Page2(QtWidgets.QWizardPage, form_wizard_page_2.Ui_Form):
    def __init__(self, parent=None, adapter=None):
        super().__init__(parent)
        self.setupUi(self)
        self.adjustSize()
        self.adapter=adapter

        self.label.setText(adapter.take_translate('pref_window', 'dbScheme'))
        self.label_receiver.setText(adapter.take_translate('pref_window', 'Target_table_name'))

        self.comboBox_dbSchema = comboBox_list_for_Page3(self.verticalLayoutWidget)
        self.comboBox_dbSchema.setObjectName("comboBox_dbSchema")
        self.horizontalLayout_16.addWidget(self.comboBox_dbSchema)

        self.target_table_name = comboBox_list_for_Page3(self.verticalLayoutWidget)
        self.target_table_name.setObjectName("target_table_name")
        self.horizontalLayout_14.addWidget(self.target_table_name)

    def validatePage(self) -> bool:
        try:
            self.wizard().page(0).pref['dbSchema'] = self.comboBox_dbSchema.currentText()
            self.wizard().page(0).pref['target_table_name'] = self.target_table_name.currentText()
        except Exception as e:
            show_alarm_window(self, "Can't save params")
            return False
        else:
            return True


class Page3(QtWidgets.QWizardPage, form_wizard_page_3.Ui_Form):
    def __init__(self, parent=None, adapter=None):
        super().__init__(parent)
        self.setupUi(self)

        self.label.setText(adapter.take_translate('Wizard', 'Page3Label'))

        self.adapter = adapter
        self.dict_pref = {
            'dictTableName': None,
            'indxDbColumn': None,
            'indxColumnDic': None,
            'colType': '---',
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
            'isPK': 'false',
            'filter_mode': 'false',
            'post_filter_mode': 'false'
        }

        self.list_of_source_cols_links = []

        self.treeWidget_of_Source = Source_tree.Source_tree(self.adapter)
        self.horizontalLayout.addWidget(self.treeWidget_of_Source)
        self.treeWidget_of_Source.actionDuplicateColumn.triggered.connect(self.addColumnField)
        self.treeWidget_of_Source.actionDuplicateReplace.triggered.connect(self.duplicateReplace)
        self.treeWidget_of_Source.actionDeleteColumn.triggered.connect(self.deleteColumn)
        self.treeWidget_of_Source.actionDeleteReplace.triggered.connect(self.deleteReplace)



    def initializePage(self) -> None:

        if not hasattr(self, "filter_db"):
            self.filter_db = ev_filt_of_Page3(parent=self.wizard().page(1).comboBox_dbSchema)
        if not hasattr(self, "filter_target"):
            self.filter_target = ev_filt_of_Page3(parent=self.wizard().page(1).target_table_name)

        self.colnames_in_receiver = [i[0] for i in Validate_res.Validate.queryForColumns_edit(
            dbtype=self.wizard().page(0).lineEdit_dbtype.currentText(),
            target_table=self.wizard().page(1).target_table_name.currentText(),
            db_base=self.wizard().page(1).comboBox_dbSchema.currentText(),
            connector=self.wizard().page(0).con,
            executor=Validate_res.Validate.executor,
            cur=self.wizard().page(0).con.cursor,
            loggerInst=self.wizard().page(0).loggerInst
        )]

        self.columns_in_source = [i for i in self.wizard().page(0).df.parse(self.wizard().page(0).comboBox_list_source_excel.currentIndex()).columns.values]

    def deleteReplace(self):
        cur_column = list(filter(lambda x: x['colName'].combo_box_name.currentText() ==
                                           self.treeWidget_of_Source.currentItem().parent().combo_box_name.currentText(),
                                 self.list_of_source_cols_links))[0]
        if len(cur_column['replace_box']) > 1:
            cur_column['replace_box'].remove(self.treeWidget_of_Source.currentItem())
        else:
            show_alarm_window(self, "You can't delete last element !!!")
            return

        self.treeWidget_of_Source.currentItem().parent().takeChild(
            self.treeWidget_of_Source.indexFromItem(self.treeWidget_of_Source.currentItem()).row())

    def deleteColumn(self):
        if len(self.list_of_source_cols_links) > 1:
            element = list(filter(lambda x: x['colName'].combo_box_name.currentText() == self.treeWidget_of_Source.currentItem().combo_box_name.currentText(), self.list_of_source_cols_links))[0]
            self.list_of_source_cols_links.remove(element)
            self.treeWidget_of_Source.takeTopLevelItem(self.treeWidget_of_Source.indexFromItem(self.treeWidget_of_Source.currentItem()).row())
        else:
            show_alarm_window(self, "You can't delete last element !!!")
            return

    def duplicateReplace(self):
        replace = source_column_editor_viewer.ReplaceRow(column_property=self.dict_pref,
                                                         parent=self.treeWidget_of_Source,
                                                         parent_widget=self.treeWidget_of_Source.currentItem().parent(),
                                                         after_widget=self.treeWidget_of_Source.currentItem(),
                                                         adapter=self.adapter)

        self.treeWidget_of_Source.addTopLevelItem(replace)
        list(filter(lambda x: x['colName'].combo_box_name.currentText() ==
                              self.treeWidget_of_Source.currentItem().parent().combo_box_name.currentText(),
                    self.list_of_source_cols_links))[0]['replace_box'].append(replace)

    def cleanupPage(self) -> None:
        self.wizard().page(1).comboBox_dbSchema.removeEventFilter(self.filter_db)
        self.wizard().page(1).target_table_name.removeEventFilter(self.filter_target)

        self.wizard().page(1).comboBox_dbSchema.check_widget = self.treeWidget_of_Source
        self.wizard().page(1).target_table_name.check_widget = self.treeWidget_of_Source
        self.wizard().page(0).comboBox_list_source_excel.widget_to_delete_sources = self.treeWidget_of_Source
        self.wizard().page(1).target_table_name.widget_to_delete_target_tables = self.wizard().page(3).treeWidget_of_Receiver

        self.wizard().page(1).comboBox_dbSchema.currentIndexChanged.connect(self.clear)
        self.wizard().page(1).target_table_name.currentIndexChanged.connect(self.clear)
        self.wizard().page(0).excelFileName.textChanged.connect(self.clear)
        self.wizard().page(0).comboBox_list_source_excel.currentIndexChanged.connect(self.clear)

        self.wizard().page(1).comboBox_dbSchema.installEventFilter(self.filter_db)
        self.wizard().page(1).target_table_name.installEventFilter(self.filter_target)



    def clear(self):
        while self.treeWidget_of_Source.topLevelItemCount() > 0:
            self.treeWidget_of_Source.takeTopLevelItem(0)
        self.list_of_source_cols_links = []


    def addColumnField(self):
        source_column_editor_viewer.create_input_column(
            tree_table=self.treeWidget_of_Source,
            db_colnames=self.colnames_in_receiver,
            column_property=self.dict_pref,
            list_of_cols=self.list_of_source_cols_links,
            indx=self.treeWidget_of_Source.indexFromItem(self.treeWidget_of_Source.currentItem()).row(),
            source_columnes=self.columns_in_source,
            adapter=self.adapter
            )



class Page4(QtWidgets.QWizardPage, form_wizard_page_4.Ui_Form):
    column_prop_template = {
        'colName': None,
        'fromExcel': 'false',
        'defaultValue': None,
        'defaultValue_mode': 'false',
        'colType': 'str',
        'ifNull': None,
        'ifNull_mode': 'false',
        'isAutoInc': 'false',
        'isConc': 'false',
        'isUpdateCondition': 'false',
        'fromDb': 'false'
    }

    def __init__(self, parent=None, adapter=None):
        super().__init__(parent)
        self.setupUi(self)
        self.adapter = adapter
        self.label.setText(adapter.take_translate('Wizard', 'Page4Label'))
        self.treeWidget_of_Receiver = Receiver_tree.Receiver_tree(self.adapter)
        self.horizontalLayout.addWidget(self.treeWidget_of_Receiver)
        self.adapter = adapter
        self.list_of_receiver_cols_links = []


    def initializePage(self) -> None:
        self.clear()
        for col in self.wizard().page(2).colnames_in_receiver:
            col_prop = copy.deepcopy(self.column_prop_template)
            col_prop['colName'] = f'{col}'

            target_column_editor_viewer.create_receiver_column(
                tree_table=self.treeWidget_of_Receiver,
                column_property=col_prop,
                list_of_cols=self.list_of_receiver_cols_links,
                adapter=self.adapter
            )

    def clear(self):
        while self.treeWidget_of_Receiver.topLevelItemCount() > 0:
            self.treeWidget_of_Receiver.takeTopLevelItem(0)
        self.list_of_receiver_cols_links = []

    # def cleanupPage(self) -> None:



    def nextId(self) -> int:
        if self.field('dictionary_state'):
            return RoadMapConfiguration.dictionary
        else:
            return RoadMapConfiguration.final_page

class Page5(QtWidgets.QWizardPage, form_wizard_page_5.Ui_Form):
    def __init__(self, parent=None, adapter=None):
        super().__init__(parent)
        self.setupUi(self)
        self.adapter=adapter
        self.label.setText(adapter.take_translate('Wizard', 'Page5Label'))
        self.list_of_dict_pref = []
        self.config_dict = {}
        self.validator = Validate_res.Validate

    def clear(self):
        while self.tree_dict.topLevelItemCount() > 0:
            self.tree_dict.takeTopLevelItem(0)
        self.list_of_dict_pref = []

    def initializePage(self) -> None:
        self.tables_in_receiver = [i[0] for i in Validate_res.Validate.queryForTableInDbList_edit(
            connector=self.wizard().page(0).con,
            dbtype=self.wizard().page(0).lineEdit_dbtype.currentText(),
            executor=Validate_res.Validate.executor,
            cur=self.wizard().page(0).con.cursor,
            loggerInst=self.wizard().page(0).loggerInst
        )]
        self.columns_in_source = self.wizard().page(2).columns_in_source

        if not hasattr(self, "tree_dict"):
            self.tree_dict = Dict_tree.DictTree(
                list_of_dict_pref=self.list_of_dict_pref,
                config=self.config_dict,
                validator=self.validator,
                tables_in_receiver=self.tables_in_receiver,
                columns_names_source=self.columns_in_source,
                dbtype=self.wizard().page(0).lineEdit_dbtype.currentText(),
                target_table=self.wizard().page(1).target_table_name.currentText(),
                db_base=self.wizard().page(1).comboBox_dbSchema.currentText(),
                connector=self.wizard().page(0).con,
                executor=Validate_res.Validate.executor,
                cur=self.wizard().page(0).con.cursor,
                loggerInst=self.wizard().page(0).loggerInst,
                adapter=self.adapter
            )

        self.horizontalLayout.addWidget(self.tree_dict)

    def cleanupPage(self) -> None:
        self.wizard().page(1).comboBox_dbSchema.dict_widget = self.tree_dict
        self.wizard().page(1).target_table_name.dict_widget = self.tree_dict
        self.wizard().page(0).comboBox_list_source_excel.dict_widget = self.tree_dict

        self.wizard().page(1).comboBox_dbSchema.currentIndexChanged.connect(self.clear)
        self.wizard().page(1).target_table_name.currentIndexChanged.connect(self.clear)
        self.wizard().page(0).excelFileName.textChanged.connect(self.clear)
        self.wizard().page(0).comboBox_list_source_excel.currentIndexChanged.connect(self.clear)



class Page6(QtWidgets.QWizardPage, form_wizard_page_6.Ui_Form):
    def __init__(self, parent=None, adapter=None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.label.setText(adapter.take_translate('Wizard', 'Page6Label'))

    def initializePage(self) -> None:
        self.obj = ObjectToCreateXML(
            pref=self.wizard().page(0).pref
            ,list_of_source_cols_links=self.wizard().page(2).list_of_source_cols_links
            ,loggerInst=self.wizard().page(0).loggerInst
            ,list_of_dict_pref=self.wizard().page(4).list_of_dict_pref
            ,list_of_receiver_cols_links=self.wizard().page(3).list_of_receiver_cols_links
            ,pref_gui=self.wizard().page(0)
        )
        self.create_xml_save = CreateXML(self.obj)
        self.create_xml_save.started.connect(lambda: self.wizard().parent().ui.statusbar.showMessage('Creating XML...'))
        self.create_xml_save.message.connect(self.print_xml)
        self.create_xml_save.error_message.connect(self.wizard().parent().error_at_create_xml)
        self.create_xml_save.start()

    def print_xml(self, tree, root):
        self.tree = tree
        self.root = root
        self.textEdit.clear()
        self.wizard().parent().ui.statusbar.showMessage(f'XML Created.')
        self.textEdit.append(xml_format.parseString(et.tostring(root)).toprettyxml(indent="    "))
        del self.obj

    def validatePage(self) -> bool:
        path_to_save = QtWidgets.QFileDialog.getSaveFileName(
            directory=os.path.join(os.getcwd(), 'config'), filter='*.xml')
        if path_to_save[0] != '':
            self.wizard().parent().write_as_xml(self.tree, self.root, path=path_to_save[0])
            return True
        return False


class RoadMapConfiguration(QtWidgets.QWizard):
    db_parameters_and_check_mode = 0
    target_table_and_db_schema = 1
    source_columns = 2
    receiver_columns = 3
    dictionary = 4
    final_page = 5


class TreeWidgetLinkedColumns(QtWidgets.QTreeWidget):
    def __init__(self, parent=None, widget_sighal=None, pref_dict=None, adapter=None):
        super().__init__(parent)

        self.pref = pref_dict
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


class comboBox_list_for_Page2(QtWidgets.QComboBox):
    def __init__(self, parent=None, check_widget=None, widget_to_delete_target_tables=None):
        super().__init__(parent)
        self.check_widget = check_widget
        self.widget_to_delete_target_tables = widget_to_delete_target_tables


class comboBox_list_for_Page3(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)


class ev_filt(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, a0, a1) -> bool:
        if a1.type() == QtCore.QEvent.MouseButtonPress:
            if self.parent().check_widget.topLevelItemCount() > 0 or \
                    (hasattr(self.parent(), "widget_to_delete_sources") and self.parent().widget_to_delete_sources.topLevelItemCount() > 0) or \
                (hasattr(self.parent(), "dict_widget") and self.parent().dict_widget.topLevelItemCount() > 0):
                result = QtWidgets.QMessageBox.question(None,
                                                        "Change list ?",
                                                        "Change list ? Linked, Source, Dictionary Columns will remove",
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


class ev_filt_of_Page3(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:
        if a1.type() == QtCore.QEvent.MouseButtonPress:
            if (hasattr(self.parent(), "check_widget") and self.parent().check_widget.topLevelItemCount() > 0) or\
                    (hasattr(self.parent(), "widget_to_delete_target_tables") and self.parent().widget_to_delete_target_tables.topLevelItemCount() > 0) or \
                    (hasattr(self.parent(), "dict_widget") and self.parent().dict_widget.topLevelItemCount() > 0):
                result = QtWidgets.QMessageBox.question(None,
                                                        "Change ?",
                                                        "Change ? Source, Target, Dictionary columns will remove",
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


class LinkedColumns(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_widget: QtWidgets.QTreeWidget, current_column, parent, target_columns, source_columns, adapter):
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


class ObjectToCreateXML:
    def __init__(self,
                 pref,
                 list_of_source_cols_links,
                 loggerInst,
                 list_of_dict_pref,
                 list_of_receiver_cols_links,
                 pref_gui
                 ):
        self.pref = pref
        self.list_of_source_cols_links = list_of_source_cols_links
        self.loggerInst = loggerInst
        self.list_of_dict_pref = list_of_dict_pref
        self.list_of_receiver_cols_links = list_of_receiver_cols_links
        self.pref_gui = pref_gui

    def __str__(self):
        return f"""
                    pref                        {self.pref }
                    list_of_source_cols_links   {self.list_of_source_cols_links}
                    loggerInst                  {self.loggerInst}
                    list_of_dict_pref           {self.list_of_dict_pref} 
                    list_of_receiver_cols_links {self.list_of_receiver_cols_links}
                    pref_gui                    {self.pref_gui}

                    id                          {id(self)}
                    """


