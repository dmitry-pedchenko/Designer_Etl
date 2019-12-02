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
import xml.etree.ElementTree as et


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
            dial_win = QtWidgets.QDialog(self)
            dial_win.setWindowModality(QtCore.Qt.ApplicationModal)
            lay = QtWidgets.QVBoxLayout()
            lay.addWidget(QtWidgets.QLabel("You can't delete last element !!!"))
            dial_win.setLayout(lay)
            dial_win.exec_()
            return

    def deleteReplace(self):
        cur_column = list(filter(lambda x: x['colName'].combo_box_name.currentText() ==
                                           self.treeWidget_of_Source.currentItem().parent().combo_box_name.currentText(),
                                 self.list_of_source_cols_links))[0]
        if len(cur_column['replace_box']) > 1:
            cur_column['replace_box'].remove(self.treeWidget_of_Source.currentItem())
        else:
            dial_win = QtWidgets.QDialog(self)
            dial_win.setWindowModality(QtCore.Qt.ApplicationModal)
            lay = QtWidgets.QVBoxLayout()
            lay.addWidget(QtWidgets.QLabel("You can't delete last element !!!"))
            dial_win.setLayout(lay)
            dial_win.exec_()
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
                dial_win = QtWidgets.QDialog(self)
                dial_win.setWindowModality(QtCore.Qt.ApplicationModal)
                lay = QtWidgets.QVBoxLayout()
                lay.addWidget(QtWidgets.QLabel("Open config !!!"))
                dial_win.setLayout(lay)
                dial_win.exec_()
                return
            self.pref_gui.show()

    def show_open_config(self):
        path_name_config = QtWidgets.QFileDialog.getOpenFileName(
            directory=os.path.join(os.getcwd(), '..', 'config'), filter='*.xml'
        )
        path = os.path.basename(path_name_config[0])

        if path:
            self.close_project_data()
            self.ui.actionConfig_Editor.setChecked(True)
            self.ui.actionConfig_Editor.triggered.emit(1)
            self.loggerInst = Logger.Log_info.getInstance(path, path)
            self.loggerInst.set_config(path)

            try:
                self.config_dict = xml_parse(path, self.loggerInst)
            except Exception as e:
                self.close_project_data()
                dial_win = QtWidgets.QDialog(self)
                dial_win.setWindowModality(QtCore.Qt.ApplicationModal)
                lay = QtWidgets.QVBoxLayout()
                lay.addWidget(QtWidgets.QLabel(e.__str__()))
                dial_win.setLayout(lay)
                dial_win.exec_()
                return

            if self.config_dict['checkMode_value'] == 'false':

                con = db_con.Connection.get_instance(self.loggerInst)
                try:
                    con.connectToTheDB(host=self.config_dict['dbHost'],
                                       user=self.config_dict['dbUser'],
                                       password=self.config_dict['dbPass'],
                                       dbname=self.config_dict['dbBase'],
                                       port=int(self.config_dict['dbPort']),
                                       dbtype=self.config_dict['dbtype']
                                       )
                    con.test_conn()
                except Exception as e:
                    self.close_project_data()
                    dial_win = QtWidgets.QDialog(self)
                    dial_win.setWindowModality(QtCore.Qt.ApplicationModal)
                    lay = QtWidgets.QVBoxLayout()
                    lay.addWidget(QtWidgets.QLabel(e.__str__()))
                    dial_win.setLayout(lay)
                    dial_win.exec_()
                    return

                connector = con.get_instance(self.loggerInst)
                self.dbService = xpc.XmlParser(path, self.loggerInst)
                self.validator = Validate_res.Validate(self.dbService, self.loggerInst, opts=None, connector=connector)
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
            else:
                self.dbService = xpc.XmlParser(path, self.loggerInst)
                self.columns_in_source = [i for i in self.dbService.dataFrame.columns.values]

            self.show_pref()

        if self.pref_gui.ui.checkBox_Dictionary.isChecked():
            self.ui.actionDictionary.setChecked(True)
            self.ui.actionDictionary.triggered.emit(1)

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
        # print(
        #     self.list_of_source_cols_links,
        #       self.list_of_receiver_cols_links,
        #       self.pref,
        #       self.list_of_dict_pref
        #       )

        list_of_types_dict_to_comboBox = {
            'String': 'str',
            'Float': 'float',
            'Integer': 'int',
            'Date': 'date',
            '---': '---'
        }

        root = et.Element('main')
        importXml = et.SubElement(root, 'importXml')
        importXml_columns = et.SubElement(importXml, 'columns')
        linkedColumns = et.SubElement(importXml, 'linkedColumns')
        withDict = et.SubElement(importXml, 'withDict')
        exportTable = et.SubElement(root, 'exportTable')
        exportTable_columns = et.SubElement(exportTable, 'columns')


        et.SubElement(root, 'dbtype').text =  f'{self.pref["dbtype"]}'
        et.SubElement(root, 'dbHost').text =  f'{self.pref["dbHost"]}'
        et.SubElement(root, 'dbUser').text =  f'{self.pref["dbUser"]}'
        et.SubElement(root, 'dbPass').text =  f'{self.pref["dbPass"]}'
        et.SubElement(root, 'dbBase').text =  f'{self.pref["dbBase"]}'
        et.SubElement(root, 'dbPort').text =  f'{self.pref["dbPort"]}'
        et.SubElement(root, 'loadMode').text =  f'{self.pref["Load Mode"]}'.lower()
        et.SubElement(root, 'dict').text =  f'{self.pref["checkBox_Dictionary"]}'.lower()
        et.SubElement(root, 'checkMode').text =  f'{self.pref["checkBox_checkMode"]}'.lower()
        et.SubElement(importXml, 'path').text = f'{self.pref["excelFileName"]}'
        et.SubElement(importXml, 'sheetNumber').text = f'{self.pref["comboBox_list_source_excel"]}'

        linkedColumns.attrib['mode'] = f'{self.pref["checkBox_checkMode"]}'.lower()
        withDict.attrib['mode'] = f'{self.pref["checkBox_checkMode"]}'.lower()

        for column in self.list_of_source_cols_links:
            column_to_add = et.SubElement(importXml_columns, 'column')

            et.SubElement(column_to_add, 'colName').text = column['colName'].combo_box_name.currentText()
            et.SubElement(column_to_add, 'colNameDb').text = column['colNameDb'].currentText()
            et.SubElement(column_to_add, 'colType').text = list_of_types_dict_to_comboBox[f'{column["colType"].currentText()}']
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



        print(et.dump(root))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
