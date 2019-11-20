from PyQt5 import QtSql


class DbConnection:
    def __init__(self, con_config):
        self.con_config = con_config
        self.connect()

    def connect(self):
        self.con = QtSql.QSqlDatabase.addDatabase('QODBC')
        self.con.setDatabaseName(f"{self.con_config['dbBase']}")
        self.con.setHostName(f"{self.con_config['dbHost']}")
        self.con.setPassword(f"{self.con_config['dbPass']}")
        self.con.setPort(int(self.con_config['dbPort']))
        self.con.setUserName(f"{self.con_config['dbUser']}")

    def open(self):
        self.con.open()

    def select(self):
        q = QtSql.QSqlQuery()
        q.exec(f"select * from {self.con_config['exportTableName_value']}")
        print(q.value(0))