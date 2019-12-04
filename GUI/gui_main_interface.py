from PyQt5 import QtWidgets, QtCore
import sys
from gui_qt import main_window
import gui_prefernces_controller
import source_column_editor_viewer
import os
from Parser.XML_parser import do_XML_parse as xml_parse
from Logger import Logger
import Source_tree
import Receiver_tree
import wizard_configuration
import target_column_editor_viewer
import Dict_tree
from dict_column_editor_viewer import create_dict_column
import Core.DAO.DB_connector as db_con
from Validate import Validate_res
from Core.DAO import XML_DAO as xpc
import xml.etree.ElementTree as et
from GUI.DAO.create_xml import create_config
from alarm_window import show_alarm_window
from error_window import show_error_window
from connection_db import CreateConnection


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.list_of_source_cols_links = []
        self.list_of_receiver_cols_links = []
        self.config_dict = {}
        self.pref = {}
        self.list_of_dict_pref = []

        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)

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

        self.tab_widget_config_editor = None
        self.tab_widget_loader = None
        self.tab_widget_dictionary = None
        self.pref_gui = None
        self.dbService = None
        self.tables_in_receiver = None
        self.schemas_in_db = None

        self.ui.actionSave.setDisabled(True)
        self.ui.actionSave_as.setDisabled(True)

        # self.ui.actionLoader.setDisabled(True)
        self.ui.actionConfig_Editor.setDisabled(True)
        self.ui.actionDictionary.setDisabled(True)
        self.ui.actionEditor.setDisabled(True)
        self.connection_tread = CreateConnection()
        self.tabWidget = QtWidgets.QTabWidget(self.ui.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.ui.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.ui.actionPreferences.triggered.connect(self.show_pref)
        self.ui.actionOpen.triggered.connect(self.show_open_config)
        self.ui.actionSave.triggered.connect(self.save_configuration)
        self.ui.actionSave_as.triggered.connect(self.save_as_configuration)
        self.ui.actionConfiguration_Wizard.triggered.connect(self.show_wizrd)
        self.ui.actionConfig_Editor.triggered.connect(self.show_config_editor)
        self.ui.actionLoader.triggered.connect(self.show_loader)
        self.ui.actionDictionary.triggered.connect(self.show_dictionary)
        self.ui.actionClose_Project.triggered.connect(self.close_project_data)
        self.connection_tread.task_done.connect(self.created_connection, QtCore.Qt.QueuedConnection)

    def close_project_data(self):

        self.setWindowTitle(f"Easy Loader")

        if self.ui.actionConfig_Editor.isChecked():
            self.ui.actionConfig_Editor.setChecked(False)
            self.ui.actionConfig_Editor.triggered.emit(0)
        if self.ui.actionDictionary.isChecked():
            self.ui.actionDictionary.setChecked(False)
            self.ui.actionDictionary.triggered.emit(0)
        if self.ui.actionLoader.isChecked():
            self.ui.actionLoader.setChecked(False)
            self.ui.actionLoader.triggered.emit(0)
        if self.ui.actionEditor.isChecked():
            self.ui.actionEditor.setChecked(False)
            self.ui.actionEditor.triggered.emit(0)

        self.list_of_source_cols_links = []
        self.list_of_receiver_cols_links = []
        self.config_dict = {}
        self.pref = {}
        self.list_of_dict_pref = []


        self.pref_gui = None
        self.dbService = None
        self.tables_in_receiver = None
        self.schemas_in_db = None

        self.tab_widget_config_editor = None
        self.tab_widget_loader = None
        self.tab_widget_dictionary = None




    def create_config_editor(self):
        if self.tab_widget_config_editor:
            pass
        else:
            self.tab_widget_config_editor = QtWidgets.QWidget()
            self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
            self.splitter.setChildrenCollapsible(False)
            self.treeWidget_of_Source = Source_tree.Source_tree()
            self.treeWidget_of_Receiver = Receiver_tree.Receiver_tree()
            self.splitter.addWidget(self.treeWidget_of_Source)
            self.splitter.addWidget(self.treeWidget_of_Receiver)
            self.horizontalLayout = QtWidgets.QHBoxLayout()
            self.horizontalLayout.addWidget(self.splitter)
            self.tab_widget_config_editor.setLayout(self.horizontalLayout)
            self.treeWidget_of_Source.actionDuplicateColumn.triggered.connect(self.addColumnField)
            self.treeWidget_of_Source.actionDuplicateReplace.triggered.connect(self.duplicateReplace)
            self.treeWidget_of_Source.actionDeleteColumn.triggered.connect(self.deleteColumn)
            self.treeWidget_of_Source.actionDeleteReplace.triggered.connect(self.deleteReplace)

        self.tabWidget.addTab(self.tab_widget_config_editor, 'Config Editor')

    def create_dictionary(self):
        if self.tab_widget_dictionary:
            pass
        else:
            self.tab_widget_dictionary = QtWidgets.QWidget()
            self.tree_dict = Dict_tree.DictTree(
                                                list_of_dict_pref=self.list_of_dict_pref,
                                                config=self.config_dict,
                                                validator=self.validator,
                                                tables_in_receiver=self.tables_in_receiver,
                                                columns_names_source=self.columns_in_source,
                                                window_pref=self.pref_gui
                                                )
            hlayout = QtWidgets.QHBoxLayout()
            hlayout.addWidget(self.tree_dict)
            self.tab_widget_dictionary.setLayout(hlayout)

            if self.config_dict['dictMode'] == 'true':
                for row in self.config_dict['withDict']:
                    create_dict_column(pref=self.list_of_dict_pref,
                                       parent=self.tree_dict,
                                       cur_dic_table_pref=row,
                                       config=self.config_dict,
                                       validator=self.validator,
                                       tables_in_receiver=self.tables_in_receiver,
                                       columns_names_source=self.columns_in_source
                                       )

        self.tabWidget.addTab(self.tab_widget_dictionary, 'Dictionary Editor')

    def create_loader(self):
        if self.tab_widget_loader:
            pass
        else:
            self.tab_widget_loader = QtWidgets.QWidget()
        #     create widget here

        self.tabWidget.addTab(self.tab_widget_loader, 'Loader')

    def show_config_editor(self):
        if self.ui.actionConfig_Editor.isChecked():
            if self.tab_widget_config_editor:
                self.tabWidget.addTab(self.tab_widget_config_editor, 'Config Editor')
            else:
                self.create_config_editor()
        else:
            self.tabWidget.removeTab(self.tabWidget.indexOf(self.tab_widget_config_editor))

    def show_dictionary(self):
        if self.ui.actionDictionary.isChecked():
            if self.tab_widget_dictionary:
                self.tabWidget.addTab(self.tab_widget_dictionary, 'Dictionary Editor')
            else:
                self.create_dictionary()
        else:
            self.tabWidget.removeTab(self.tabWidget.indexOf(self.tab_widget_dictionary))

    def show_loader(self):
        if self.ui.actionLoader.isChecked():
            if self.tab_widget_loader:
                self.tabWidget.addTab(self.tab_widget_loader, 'Loader')
            else:
                self.create_loader()
        else:
            self.tabWidget.removeTab(self.tabWidget.indexOf(self.tab_widget_loader))

    def deleteColumn(self):
        if len(self.list_of_source_cols_links) > 1:
            element = list(filter(lambda x: x['colName'].combo_box_name.currentText() == self.treeWidget_of_Source.currentItem().combo_box_name.currentText(), self.list_of_source_cols_links))[0]
            self.list_of_source_cols_links.remove(element)
            self.treeWidget_of_Source.takeTopLevelItem(self.treeWidget_of_Source.indexFromItem(self.treeWidget_of_Source.currentItem()).row())
        else:
            show_alarm_window(self,"You can't delete last element !!!")
            return

    def deleteReplace(self):
        cur_column = list(filter(lambda x: x['colName'].combo_box_name.currentText() ==
                                           self.treeWidget_of_Source.currentItem().parent().combo_box_name.currentText(),
                                 self.list_of_source_cols_links))[0]
        if len(cur_column['replace_box']) > 1:
            cur_column['replace_box'].remove(self.treeWidget_of_Source.currentItem())
        else:
            show_alarm_window(self, "You can't delete last element !!!")
            return

        self.treeWidget_of_Source.currentItem().parent().takeChild(self.treeWidget_of_Source.indexFromItem(self.treeWidget_of_Source.currentItem()).row())

    def show_wizrd(self):
        self.wizard = wizard_configuration.WizardConfig()
        self.wizard.show()

    def show_pref(self):
        if self.pref_gui:
            self.pref_gui.show()
        else:
            try:
                self.pref_gui = gui_prefernces_controller.Pref_Window(main_gui_widget=self,
                                                                      config_dict=self.config_dict,
                                                                      pref=self.pref,
                                                                      dbService=self.dbService,
                                                                      logger_inst=self.loggerInst,
                                                                      tables_in_db=self.tables_in_receiver,
                                                                      schemas_in_db=self.schemas_in_db,
                                                                      parent=self.pref_gui
                                                                      )
            except Exception as e:
                show_alarm_window(self, "Open config !!!")
                return
            self.pref_gui.show()

    def created_connection(self, conn):
        print(conn)
        self.connector = conn

    def show_open_config(self):
        self.path_name_config = QtWidgets.QFileDialog.getOpenFileName(
            directory=os.path.join(os.getcwd(), '..', 'config'), filter='*.xml')
        self.path = os.path.basename(self.path_name_config[0])




        if self.path:
            self.close_project_data()
            self.setWindowTitle(f"Easy Loader [{self.path}]")
            self.ui.actionConfig_Editor.setChecked(True)
            self.ui.actionConfig_Editor.triggered.emit(1)
            self.loggerInst = Logger.Log_info.getInstance(self.path, self.path)
            self.loggerInst.set_config(self.path)

            try:
                self.config_dict = xml_parse(self.path, self.loggerInst)
            except Exception as e:
                show_error_window(self, e.__str__())
                self.close_project_data()
                return

            # if self.config_dict['checkMode_value'] == 'false':

            # con = db_con.Connection.get_instance(self.loggerInst)
            #             # try:
            #             #     con.connectToTheDB(host=self.config_dict['dbHost'],
            #             #                        user=self.config_dict['dbUser'],
            #             #                        password=self.config_dict['dbPass'],
            #             #                        dbname=self.config_dict['dbBase'],
            #             #                        port=int(self.config_dict['dbPort']),
            #             #                        dbtype=self.config_dict['dbtype']
            #             #                        )
            #             #     con.test_conn()
            #             # except Exception as e:
            #             #     show_error_window(self, e.__str__())
            #             #     self.close_project_data()
            #             #     return
            #             #
            #             # connector = con.get_instance(self.loggerInst)

            self.connection_tread.start()
            # CreateConnection.wait(self.connection_tread)

            while self.connection_tread.isRunning():
                self.ui.statusbar.showMessage('Connecting...')
            self.ui.statusbar.showMessage('Connected')

            try:
                self.dbService = xpc.XmlParser(self.path, self.loggerInst)
            except Exception as e:
                show_error_window(self, f"Can't parse Excel file\n{e} !!!")
                self.close_project_data()
                return

            self.validator = Validate_res.Validate(self.dbService, self.loggerInst, opts=None, connector=self.connector)
            self.columns_in_db = self.validator.queryForColumns()
            self.columns_in_source = [i for i in self.dbService.dataFrame.columns.values]
            self.colnames_of_receiver = [i[0] for i in self.columns_in_db]
            self.tables_in_receiver = [i[0] for i in self.validator.queryForTableInDbList()]
            self.schemas_in_db = [i[0] for i in self.validator.queryForSchemasInDb()]

            for col in self.config_dict['excelColumns']:
                source_column_editor_viewer.create_input_column(self.treeWidget_of_Source,
                                                                self.colnames_of_receiver,
                                                                col,
                                                                list_of_cols=self.list_of_source_cols_links,
                                                                source_columnes=self.columns_in_source
                                                                )
            for col in self.config_dict['dbColumns']:
                target_column_editor_viewer.create_receiver_column(
                    self.treeWidget_of_Receiver,
                    col,
                    list_of_cols=self.list_of_receiver_cols_links
                )
            # else:
            #     self.dbService = xpc.XmlParser(self.path, self.loggerInst)
            #     self.columns_in_source = [i for i in self.dbService.dataFrame.columns.values]
            #
            #     con = db_con.Connection.get_instance(self.loggerInst)
            #     try:
            #         con.connectToTheDB(host=self.config_dict['dbHost'],
            #                            user=self.config_dict['dbUser'],
            #                            password=self.config_dict['dbPass'],
            #                            dbname=self.config_dict['dbBase'],
            #                            port=int(self.config_dict['dbPort']),
            #                            dbtype=self.config_dict['dbtype']
            #                            )
            #         con.test_conn()
            #     except Exception as e:
            #         show_error_window(self, e.__str__())
            #         self.close_project_data()
            #         return
            #
            #     connector = con.get_instance(self.loggerInst)
            #     try:
            #         self.dbService = xpc.XmlParser(self.path, self.loggerInst)
            #     except Exception as e:
            #         show_error_window(self, f"Can't parse Excel file\n{e} !!!")
            #         self.close_project_data()
            #         return
            #
            #     self.validator = Validate_res.Validate(self.dbService, self.loggerInst, opts=None, connector=connector)
            #     self.columns_in_db = self.validator.queryForColumns()
            #     self.colnames_of_receiver = [i[0] for i in self.columns_in_db]
            #
            #     for col in self.config_dict['excelColumns']:
            #         source_column_editor_viewer.create_input_column(self.treeWidget_of_Source,
            #                                                         self.colnames_of_receiver,
            #                                                         col,
            #                                                         list_of_cols=self.list_of_source_cols_links,
            #                                                         source_columnes=self.columns_in_source
            #                                                         )

            self.show_pref()

            if self.pref_gui.ui.checkBox_Dictionary.isChecked():
                self.ui.actionDictionary.setChecked(True)
                self.ui.actionDictionary.triggered.emit(1)

            self.ui.actionSave.setDisabled(False)
            self.ui.actionSave_as.setDisabled(False)

    def addColumnField(self):
        source_column_editor_viewer.create_input_column(
            tree_table=self.treeWidget_of_Source,
            db_colnames=self.colnames_of_receiver,
            column_property=self.dict_pref,
            list_of_cols=self.list_of_source_cols_links,
            indx=self.treeWidget_of_Source.indexFromItem(self.treeWidget_of_Source.currentItem()).row(),
            source_columnes=self.columns_in_source
            )

    def duplicateReplace(self):
        replace = source_column_editor_viewer.ReplaceRow(column_property=self.dict_pref,
                                                         parent=self.treeWidget_of_Source,
                                                         parent_widget=self.treeWidget_of_Source.currentItem().parent(),
                                                         after_widget=self.treeWidget_of_Source.currentItem())

        self.treeWidget_of_Source.addTopLevelItem(replace)
        list(filter(lambda x: x['colName'].combo_box_name.currentText() ==
                              self.treeWidget_of_Source.currentItem().parent().combo_box_name.currentText(),
                    self.list_of_source_cols_links))[0]['replace_box'].append(replace)

    def save_configuration(self):
        create_config(self.path_name_config[0], self)

    def save_as_configuration(self):
        path_to_save = QtWidgets.QFileDialog.getSaveFileName(
            directory=os.path.join(os.getcwd(), '..', 'config'), filter='*.xml')
        create_config(f"{path_to_save[0]}", self)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
