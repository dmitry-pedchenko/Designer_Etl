from PyQt5 import QtWidgets, QtCore
import sys
from gui_qt import main_window
from gui_qt import form_preferences
import os

class Pref_Window(QtWidgets.QWidget):
    def __init__(self, list_of_db_pref: dict, config_dict: list):
        super().__init__()
        self.pref = {}
        self.config_dict = config_dict
        self.list_of_db_pref = list_of_db_pref
        self.ui = form_preferences.Ui_Form()
        self.ui.setupUi(self)
        self.ui.comboBox_chose_loadMode.insertItem(0, 'insert')
        self.ui.comboBox_chose_loadMode.insertItem(1, 'update')
        list_of_db_types = ['mysql', 'mssql']
        self.ui.lineEdit_dbtype.addItems(list_of_db_types)

        if config_dict:
            self.initialize()

        self.ui.button_save_pref.clicked.connect(self.save_db_pref)

        self.ui.lineEdit_dbtype.currentIndexChanged.connect(self.add_asterisc_dbtype)
        self.ui.lineEdit_dbhost.textChanged.connect(self.add_asterisc_dbhost)
        self.ui.lineEdit_dbuser.textChanged.connect(self.add_asterisc_dbuser)
        self.ui.lineEdit_dbpass.textChanged.connect(self.add_asterisc_dbpass)
        self.ui.lineEdit_dbbase.textChanged.connect(self.add_asterisc_dbbase)
        self.ui.lineEdit_dbport.textChanged.connect(self.add_asterisc_dbport)
        self.ui.checkBox_checkMode.stateChanged.connect(self.add_asterisc_checkBox_checkMode)
        self.ui.comboBox_chose_loadMode.currentIndexChanged.connect(self.add_asterisc_loadMode)
        self.ui.open_excel_file.clicked.connect(self.open_excel_folder)

    def initialize(self):
        if self.list_of_db_pref:
            pass
        else:
            self.ui.lineEdit_dbtype.setCurrentText(self.config_dict['dbtype'])
            self.ui.lineEdit_dbport.setText(self.config_dict['dbPort'])
            self.ui.lineEdit_dbbase.setText(self.config_dict['dbBase'])
            self.ui.lineEdit_dbpass.setText(self.config_dict['dbPass'])
            self.ui.lineEdit_dbuser.setText(self.config_dict['dbUser'])
            self.ui.lineEdit_dbhost.setText(self.config_dict['dbHost'])
            self.ui.excelFileName.setText(self.config_dict['importXml_path_value'])
            self.ui.comboBox_chose_loadMode.setCurrentText(self.config_dict['loadMode'])
            self.ui.target_table_name.setText(self.config_dict['exportTableName_value'])

            if self.config_dict['checkMode_value'] == 'true':
                self.ui.checkBox_checkMode.setCheckState(QtCore.Qt.Checked)
            else:
                self.ui.checkBox_checkMode.setCheckState(QtCore.Qt.Unchecked)

    def add_asterisc_dbtype(self):
        if self.ui.label_dbtype.text()[0] != '*':
            self.ui.label_dbtype.setText(f"*{self.ui.label_dbtype.text()}")

    def add_asterisc_dbhost(self):
        if self.ui.label_dbHost.text()[0] != '*':
            self.ui.label_dbHost.setText(f"*{self.ui.label_dbHost.text()}")

    def add_asterisc_dbuser(self):
        if self.ui.label_dbUser.text()[0] != '*':
            self.ui.label_dbUser.setText(f"*{self.ui.label_dbUser.text()}")

    def add_asterisc_dbpass(self):
        if self.ui.label_dbPass.text()[0] != '*':
            self.ui.label_dbPass.setText(f"*{self.ui.label_dbPass.text()}")

    def add_asterisc_dbbase(self):
        if self.ui.label_dbBase.text()[0] != '*':
            self.ui.label_dbBase.setText(f"*{self.ui.label_dbBase.text()}")

    def add_asterisc_dbport(self):
        if self.ui.label_dbPort.text()[0] != '*':
            self.ui.label_dbPort.setText(f"*{self.ui.label_dbPort.text()}")

    def add_asterisc_checkBox_checkMode(self):
        if self.ui.checkBox_checkMode.text()[0] != '*':
            self.ui.checkBox_checkMode.setText(f"*{self.ui.checkBox_checkMode.text()}")

    def add_asterisc_loadMode(self):
        if self.ui.label_loadMode.text()[0] != '*':
            self.ui.label_loadMode.setText(f"*{self.ui.label_loadMode.text()}")



    def save_db_pref(self):

        if self.pref:
            pass
        else:
            self.pref['dbtype'] = self.ui.lineEdit_dbtype.currentText()
            self.pref['dbHost'] = self.ui.lineEdit_dbhost.text()
            self.pref['dbUser'] = self.ui.lineEdit_dbuser.text()
            self.pref['dbPass'] = self.ui.lineEdit_dbpass.text()
            self.pref['dbBase'] = self.ui.lineEdit_dbbase.text()
            self.pref['dbPort'] = self.ui.lineEdit_dbport.text()
            self.pref['checkBox_checkMode'] = bool(self.ui.checkBox_checkMode.checkState())
            self.pref['comboBox_chose_loadMode'] = self.ui.comboBox_chose_loadMode.currentText()

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

        if self.ui.label_loadMode.text()[0] == '*':
            self.ui.label_loadMode.setText(f"{self.ui.label_loadMode.text()[1:]}")
            self.ui.label_loadMode.adjustSize()

    def open_excel_folder(self):
        path_name = QtWidgets.QFileDialog.getOpenFileName(directory=os.path.join(os.getcwd(), '..', 'Source'),
                                                                 filter='*.xlsx')
        path = os.path.basename(path_name[0])
        self.ui.excelFileName.setText(path)