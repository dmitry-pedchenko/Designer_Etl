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
from DAO import XML_DAO as xpc


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.list_of_source_cols_links = []
        self.list_of_receiver_cols_links = []
        self.config_dict = {}
        self.list_of_db_pref = {}
        self.pref = {}
        self.list_of_dict_pref = []

        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.tab_widget_config_editor = None
        self.tab_widget_loader = None
        self.tab_widget_dictionary = None

        self.tabWidget = QtWidgets.QTabWidget(self.ui.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.ui.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.ui.actionPreferences.triggered.connect(self.show_pref)
        self.ui.actionOpen.triggered.connect(self.show_open_config)
        self.ui.actionSave.triggered.connect(self.save_configuration)
        self.ui.actionConfiguration_Wizard.triggered.connect(self.show_wizrd)
        self.ui.actionConfig_Editor.triggered.connect(self.show_config_editor)
        self.ui.actionLoader.triggered.connect(self.show_loader)
        self.ui.actionDictionary.triggered.connect(self.show_dictionary)
        self.ui.actionClose_Project.triggered.connect(self.close_project_data)

    def close_project_data(self):

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
        self.list_of_db_pref = {}
        self.pref = {}
        self.list_of_dict_pref = []

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
            self.treeWidget_1 = Source_tree.Source_tree()
            self.treeWidget_2 = Receiver_tree.Receiver_tree()
            self.splitter.addWidget(self.treeWidget_1)
            self.splitter.addWidget(self.treeWidget_2)
            self.horizontalLayout = QtWidgets.QHBoxLayout()
            self.horizontalLayout.addWidget(self.splitter)
            self.tab_widget_config_editor.setLayout(self.horizontalLayout)
            self.treeWidget_1.actionDuplicateColumn.triggered.connect(self.duplicateColumn)
            self.treeWidget_1.actionDuplicateReplace.triggered.connect(self.duplicateReplace)
            self.treeWidget_1.actionDeleteColumn.triggered.connect(self.deleteColumn)
            self.treeWidget_1.actionDeleteReplace.triggered.connect(self.deleteReplace)

        self.tabWidget.addTab(self.tab_widget_config_editor, 'Config Editor')

    def create_dictionary(self):
        if self.tab_widget_dictionary:
            pass
        else:
            self.tab_widget_dictionary = QtWidgets.QWidget()
            self.tree_dict = Dict_tree.DictTree(self.list_of_dict_pref)
            hlayout = QtWidgets.QHBoxLayout()
            hlayout.addWidget(self.tree_dict)
            self.tab_widget_dictionary.setLayout(hlayout)

            for row in self.config_dict['withDict']:
                create_dict_column(self.list_of_dict_pref, parent=self.tree_dict, cur_column_pref=row)

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
        element = list(filter(lambda x: x['colName'].col_name == self.treeWidget_1.currentItem().col_name, self.list_of_source_cols_links))[0]
        self.list_of_source_cols_links.remove(element)
        self.treeWidget_1.takeTopLevelItem(self.treeWidget_1.indexFromItem(self.treeWidget_1.currentItem()).row())

    def deleteReplace(self):
        cur_column = list(filter(lambda x: x['colName'].col_name == self.treeWidget_1.currentItem().parent().col_name, self.list_of_source_cols_links))[0]
        cur_column['replace_box'].remove(self.treeWidget_1.currentItem())
        self.treeWidget_1.currentItem().parent().takeChild(self.treeWidget_1.indexFromItem(self.treeWidget_1.currentItem()).row())

    def show_wizrd(self):
        self.wizard = wizard_configuration.WizardConfig()
        self.wizard.show()

    def show_pref(self):
        self.pref_gui = gui_prefernces_controller.Pref_Window(self, self.list_of_db_pref, self.config_dict, self.pref, self.dbService, self.loggerInst)
        self.pref_gui.show()

    def show_open_config(self):
        path_name_config = QtWidgets.QFileDialog.getOpenFileName(directory=os.path.join(os.getcwd(), '..', 'config'), filter='*.xml')
        path = os.path.basename(path_name_config[0])

        if path:
            self.close_project_data()
            self.ui.actionConfig_Editor.setChecked(True)
            self.ui.actionConfig_Editor.triggered.emit(1)
            self.loggerInst = Logger.Log_info.getInstance(path, path)
            self.loggerInst.set_config(path)

            self.config_dict = xml_parse(path, self.loggerInst)

            if self.config_dict['checkMode_value'] == 'false':

                con = db_con.Connection.get_instance(self.loggerInst)
                con.connectToTheDB(host=self.config_dict['dbHost'],
                                   user=self.config_dict['dbUser'],
                                   password=self.config_dict['dbPass'],
                                   dbname=self.config_dict['dbBase'],
                                   port=int(self.config_dict['dbPort']),
                                   dbtype=self.config_dict['dbtype']
                                   )
                con.test_conn()
                connector = con.get_instance(self.loggerInst)
                self.dbService = xpc.XmlParser(path, self.loggerInst)
                validator = Validate_res.Validate(self.dbService, self.loggerInst, opts=None, connector=connector)
                self.columns_in_db = validator.queryForColumns()
                self.columns_in_source = [i for i in self.dbService.dataFrame.columns.values]

                self.colnames_of_receiver = [i[0] for i in self.columns_in_db]

                for col in self.config_dict['excelColumns']:
                    source_column_editor_viewer.create_input_column(self.treeWidget_1,
                                                                self.colnames_of_receiver,
                                                                col,
                                                                list_of_cols=self.list_of_source_cols_links,
                                                                source_columnes=self.columns_in_source
                                                                    )
                for col in self.config_dict['dbColumns']:
                    target_column_editor_viewer.create_receiver_column(
                        self.treeWidget_2,
                        col,
                        list_of_cols=self.list_of_receiver_cols_links
                    )
            self.show_pref()



        if self.pref_gui.ui.checkBox_Dictionary.isChecked():
            self.ui.actionDictionary.setChecked(True)
            self.ui.actionDictionary.triggered.emit(1)


    def duplicateColumn(self):
        source_column_editor_viewer.create_input_column(self.treeWidget_1,
                                                        self.colnames_of_receiver,
                                                        self.treeWidget_1.currentItem().column_property,
                                                        list_of_cols=self.list_of_source_cols_links,
                                                        indx=self.treeWidget_1.indexFromItem(self.treeWidget_1.currentItem()).row(),
                                                        source_columnes=self.columns_in_source
                                                        )

    def duplicateReplace(self):
        replace = source_column_editor_viewer.ReplaceRow(self.treeWidget_1.currentItem().column_property,
                                                         self.treeWidget_1,
                                                         self.treeWidget_1.currentItem().parent(),
                                                         after_widget=self.treeWidget_1.currentItem())

        self.treeWidget_1.addTopLevelItem(replace)
        list(filter(lambda x: x['colName'].col_name == self.treeWidget_1.currentItem().parent().col_name, self.list_of_source_cols_links))[0]['replace_box'].append(replace)

    def save_configuration(self):
        print(self.list_of_source_cols_links,
              self.list_of_receiver_cols_links
              )




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
