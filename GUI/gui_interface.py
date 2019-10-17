from PyQt5 import QtWidgets, QtCore
import sys
from gui_qt import form
from gui_qt import form_preferences
import gui_prefernces_controller
import input_column_editor_viewer
import os
from Parser.XML_parser import do_XML_parse as xml_parse
from Logger import Logger
import Source_tree
import wizard_configuration
import target_column_editor_viewer

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.list_of_source_cols_links = []
        self.list_of_receiver_cols_links = []
        self.list_of_db_pref = {}
        self.ui = form.Ui_MainWindow()
        self.ui.setupUi(self)
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.config_dict = []
        self.treeWidget_1 = Source_tree.Source_tree()
        # self.treeWidget_1.headerItem().setText(0, "Source rows")

        self.treeWidget_2 = QtWidgets.QTreeWidget()
        self.treeWidget_2.headerItem().setText(0, "Target rows")

        self.splitter.addWidget(self.treeWidget_1)
        self.splitter.addWidget(self.treeWidget_2)

        self.ui.horizontalLayout.addWidget(self.splitter)

        self.ui.actionPreferences.triggered.connect(self.show_pref)
        self.ui.actionOpen.triggered.connect(self.show_open_config)

        self.treeWidget_1.actionDuplicateColumn.triggered.connect(self.duplicateColumn)
        self.treeWidget_1.actionDuplicateReplace.triggered.connect(self.duplicateReplace)
        self.ui.actionSave.triggered.connect(self.save_configuration)
        self.ui.actionConfiguration_Wizard.triggered.connect(self.show_wizrd)
        self.treeWidget_1.actionDeleteColumn.triggered.connect(self.deleteColumn)

    def deleteColumn(self):
        element = list(filter(lambda x: x['colName'].col_name == self.treeWidget_1.currentItem().col_name, self.list_of_source_cols_links))[0]
        self.list_of_source_cols_links.remove(element)
        self.treeWidget_1.takeTopLevelItem(self.treeWidget_1.indexFromItem(self.treeWidget_1.currentItem()).row())

    def show_wizrd(self):
        self.wizard = wizard_configuration.WizardConfig()
        self.wizard.show()



    def show_pref(self):
        self.pref = gui_prefernces_controller.Pref_Window(self.list_of_db_pref, self.config_dict)
        self.pref.show()

    def show_open_config(self):
        path_name_config = QtWidgets.QFileDialog.getOpenFileName(directory=os.path.join(os.getcwd(), '..', 'config'), filter='*.xml')
        path = os.path.basename(path_name_config[0])

        self.loggerInst = Logger.Log_info.getInstance(path, path)
        self.loggerInst.set_config(path)

        self.config_dict = xml_parse(path, self.loggerInst)

        # test vars
        self.colnames_of_receiver = [name['colName'] for name in self.config_dict['dbColumns']]
        # --- --- ---

        for col in self.config_dict['excelColumns']:
            input_column_editor_viewer.create_input_column(self.treeWidget_1,
                                                           self.colnames_of_receiver,
                                                           col,
                                                           list_of_cols=self.list_of_source_cols_links)
        for col in self.config_dict['dbColumns']:
            target_column_editor_viewer.create_receiver_column(
                self.treeWidget_2,
                self.colnames_of_receiver,
                col,
                self.list_of_receiver_cols_links
            )


    def duplicateColumn(self):
        print(self.treeWidget_1.indexFromItem(self.treeWidget_1.currentItem()).row())
        input_column_editor_viewer.create_input_column(self.treeWidget_1,
                                                       self.colnames_of_receiver,
                                                       self.treeWidget_1.currentItem().column_property,
                                                       list_of_cols=self.list_of_source_cols_links,
                                                       index=self.treeWidget_1.indexFromItem(self.treeWidget_1.currentItem()).row())

    def duplicateReplace(self):
        replace = input_column_editor_viewer.ReplaceRow(self.treeWidget_1.currentItem().column_property,
                                              self.treeWidget_1,
                                              self.treeWidget_1.currentItem().parent(),
                                            after_widget=self.treeWidget_1.currentItem())

        self.treeWidget_1.addTopLevelItem(replace)

        list(filter(lambda x: x['colName'].col_name == self.treeWidget_1.currentItem().parent().col_name, self.list_of_source_cols_links))[0]['replace_box'].append(replace)


    def save_configuration(self):
        print(self.list_of_source_cols_links)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
