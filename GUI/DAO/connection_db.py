import Core.DAO.DB_connector as db_con
from PyQt5 import QtCore


class CreateConnection(QtCore.QThread):
    task_done = QtCore.pyqtSignal(object)
    task_done_error = QtCore.pyqtSignal(object)

    def __init__(self, main_window) -> None:
        super().__init__()
        self.main_window = main_window

    def run(self) -> None:
        con = db_con.Connection.get_instance(self.main_window.loggerInst)
        try:
            con.connectToTheDB(host=self.main_window.config_dict['dbHost'],
                               user=self.main_window.config_dict['dbUser'],
                               password=self.main_window.config_dict['dbPass'],
                               dbname=self.main_window.config_dict['dbBase'],
                               port=int(self.main_window.config_dict['dbPort']),
                               dbtype=self.main_window.config_dict['dbtype']
                               )
            con.test_conn()
        except Exception as e:
            self.task_done_error.emit(e)
        else:
            connector = con.get_instance(self.main_window.loggerInst)
            self.task_done.emit(connector)