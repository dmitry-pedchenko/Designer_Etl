from PyQt5 import QtWidgets, QtCore
import GUI.gui_qt.loader as loader
import os
import platform
import subprocess
from Core.Main_excel_parser import MainLoader
from GUI.Windows import alarm_window
from GUI.Windows.alarm_window import show_alarm_window
from GUI.Windows.error_window import show_error_window


class EasyLoader(QtWidgets.QWidget, loader.Ui_Form):
    def __init__(self, parent=None, adapter=None):
        super().__init__(parent)
        self.setupUi(self)
        self.adapter=adapter

        self.radioButton.setText(f"{adapter.take_translate('EasyLoader', 'TestMode')}")
        self.radioButton_2.setText(f"{adapter.take_translate('EasyLoader', 'LoadMode')}")
        self.label.setText(f"{adapter.take_translate('EasyLoader', 'ConfigName')}")
        self.pushButton_logs.setText(f"{adapter.take_translate('EasyLoader', 'LogsFolder')}")
        self.pushButton_start.setText(f"{adapter.take_translate('EasyLoader', 'Start')}")

        self.text_edit_log = QtWidgets.QTextEdit(self.Log)
        self.text_edit_log.setGeometry(QtCore.QRect(0, 0, 961, 401))
        self.text_edit_log.setReadOnly(True)
        self.text_edit_log.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.text_edit_debug = QtWidgets.QTextEdit(self.Debug)
        self.text_edit_debug.setGeometry(QtCore.QRect(0, 0, 961, 401))
        self.text_edit_debug.setReadOnly(True)
        self.text_edit_debug.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)


        currentPath = os.getcwd()
        self.log_path = os.path.join(currentPath, 'log')

        for i in os.listdir(os.path.join(currentPath, 'config')):
            self.comboBox.addItem(i)
        self.comboBox.addItem('---')
        self.comboBox.setCurrentText('---')

        self.pushButton_logs.clicked.connect(self.open_logs)
        self.radioButton.toggled.connect(self.check1)
        self.radioButton_2.toggled.connect(self.check2)
        self.comboBox.activated.connect(self.on_combox)
        self.pushButton_start.clicked.connect(self.pre_on_start)

    def pre_on_start(self):
        if self.comboBox.currentText() == '---':
            show_alarm_window(self, 'Select configuration file !!!')
            return
        elif not hasattr(self, 'mode'):
            show_alarm_window(self, 'Select loading mode !!!')
            return
        else:
            self.on_start(config_path=self.config_path, mode=self.mode)


    def on_combox(self):
        self.config_path = self.comboBox.currentText()

    def open_logs(self):
        self.open_file(self.log_path)

    def check1(self):
        if self.radioButton.isChecked():
            self.mode = 'true'
            self.pushButton_start.setText(f"{self.adapter.take_translate('EasyLoader', 'Test')}")

    def check2(self):
        if self.radioButton_2.isChecked():
            self.mode = 'false'
            self.pushButton_start.setText(f"{self.adapter.take_translate('EasyLoader', 'Start')}")

    def open_file(self, path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])

    def on_start(self, config_path, mode):
        self.text_edit_debug.clear()
        self.text_edit_log.clear()

        self.loader = MainLoader(path=config_path, mode=mode, parent=self)
        self.loader.pyqt_signal_debug.connect(self.write_debug)
        self.loader.pyqt_signal_log.connect(self.write_log)
        self.loader.pyqt_signal_error.connect(self.show_message)
        self.loader.started.connect(self.set_disable_window)
        self.loader.finished.connect(self.set_enabled_window)

        self.loader.start()

    def set_disable_window(self):
        self.window().ui.statusbar.showMessage(f'Executing ...')
        self.radioButton.setDisabled(True)
        self.radioButton_2.setDisabled(True)
        self.pushButton_start.setDisabled(True)
        self.pushButton_logs.setDisabled(True)
        self.comboBox.setDisabled(True)

    def set_enabled_window(self):
        self.window().ui.statusbar.showMessage(f'Complete.')

        self.radioButton.setDisabled(False)
        self.radioButton_2.setDisabled(False)
        self.pushButton_start.setDisabled(False)
        self.pushButton_logs.setDisabled(False)
        self.comboBox.setDisabled(False)

    def write_debug(self, str):
        self.text_edit_debug.append(str)

    def write_log(self, str):
        self.text_edit_log.append(str)

    def show_message(self, message):
        show_error_window(self, message)
