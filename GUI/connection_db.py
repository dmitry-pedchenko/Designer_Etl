import typing
from error_window import show_error_window
from PyQt5.QtCore import QObject
import time
import Core.DAO.DB_connector as db_con
from PyQt5 import QtWidgets, QtCore


class CreateConnection(QtCore.QThread):
    task_done = QtCore.pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        self.task_done.emit('s')
        # con = db_con.Connection.get_instance(self.main_window.loggerInst)
        # try:
        #     con.connectToTheDB(host=self.main_window.config_dict['dbHost'],
        #                        user=self.main_window.config_dict['dbUser'],
        #                        password=self.main_window.config_dict['dbPass'],
        #                        dbname=self.main_window.config_dict['dbBase'],
        #                        port=int(self.main_window.config_dict['dbPort']),
        #                        dbtype=self.main_window.config_dict['dbtype']
        #                        )
        #     con.test_conn()
        # except Exception as e:
        #     show_error_window(self.main_window, e.__str__())
        #     self.main_window.close_project_data()
        #     return
        # connector = con.get_instance(self.main_window.loggerInst)
        # self.task_done.emit(connector)