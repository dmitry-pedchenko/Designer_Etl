import pymssql as p
import time
import mysql.connector



class Connection:
    __instance = None

    @classmethod
    def get_instance(cls, log, host, user, password, dbname, port, dbtype):
        if not cls.__instance:
            cls.__instance = Connection(log, host, user, password, dbname, port, dbtype)
        return cls.__instance

    def __init__(self,log, host, user, password, dbname, port, dbtype):
        self.connectToTheDB(log, host, user, password, dbname, port, dbtype)

    def connectToTheDB(self, log, host, user, password, dbname, port, dbtype):
        self.log = log
        if dbtype == 'mssql':
            try:
                self.conn = p.connect(host=host, port=port, user=user, password=password, database=dbname)
                self.cursor = self.conn.cursor()
            except:
                log.raiseError(18, host, dbname, user, port)

        if dbtype == 'mysql':
            try:
                self.conn = mysql.connector.connect(host=host, port=port, user=user, password=password, database=dbname)
                self.cursor = self.conn.cursor()
            except:
                log.raiseError(18, host, dbname, user, port)

        log.raiseInfo(2, host, port, dbname)

    def closeConnect(self):
        try:
            self.conn.close()
            self.log.raiseInfo(3)
        except:
            self.log.raiseError(19)

    def get_conn(self):
        return self.conn

    def get_cur(self):
        return self.cursor

    def test_conn(self, attempt):
        query = """SELECT 1"""

        has_try = False
        counter_attempt = 0
        while not has_try:
            try:
                self.exec(query)
                has_try = True
            except Exception as e:
                if counter_attempt <= attempt:
                    counter_attempt += 1
                    self.log.raiseInfo(15, e.args[0])
                    self.log.raiseInfo(16, counter_attempt)
                    self.log.raiseInfo(14, 120)
                    time.sleep(120)
                else:
                    self.log.raiseError(38, e.args[0])

    def exec(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            self.log.raiseError(38, e.args[1])
            self.closeConnect()