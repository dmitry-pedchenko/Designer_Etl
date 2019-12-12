import pymssql as p
import time
import mysql.connector

class Connection:
    __instance = None
    connection_arr = []

    @classmethod
    def get_instance(cls, log=None):
        if not cls.__instance:
            cls.__instance = Connection(log)
        return cls.__instance

    def __init__(self, log):
        self.log = log

    def connectToTheDB(self, host, user, password, dbname, port, dbtype):
        if len(self.connection_arr) == 0:
            if dbtype == 'mssql':
                try:
                    self.conn = p.connect(host=host, port=port, user=user, password=password, database=dbname)
                    self.cursor = self.conn.cursor()
                    self.connection_arr.append({'dbtype': 'mssql', 'conn': self.conn, 'cursor': self.cursor})
                except:
                    self.log.raiseError(18, host, dbname, user, port)

            if dbtype == 'mysql':
                try:
                    self.conn = mysql.connector.connect(host=host, port=port, user=user, password=password,
                                                        database=dbname)
                    self.cursor = self.conn.cursor()
                    self.connection_arr.append({'dbtype': 'mysql', 'conn': self.conn, 'cursor': self.cursor})
                except:
                    self.log.raiseError(18, host, dbname, user, port)
        else:
            if dbtype in [x['dbtype'] for x in self.connection_arr]:
                self.conn = list(filter(lambda x: x['dbtype'] == dbtype ,self.connection_arr))[0]['conn']
                self.cursor = list(filter(lambda x: x['dbtype'] == dbtype ,self.connection_arr))[0]['cursor']
            else:
                if dbtype == 'mssql':
                    try:
                        self.conn = p.connect(host=host, port=port, user=user, password=password, database=dbname)
                        self.cursor = self.conn.cursor()
                        self.connection_arr.append({'dbtype': 'mssql', 'conn': self.conn, 'cursor': self.cursor})
                    except:
                        self.log.raiseError(18, host, dbname, user, port)

                if dbtype == 'mysql':
                    try:
                        self.conn = mysql.connector.connect(host=host, port=port, user=user, password=password,
                                                            database=dbname)
                        self.cursor = self.conn.cursor()
                        self.connection_arr.append({'dbtype': 'mysql', 'conn': self.conn, 'cursor': self.cursor})
                    except:
                        self.log.raiseError(18, host, dbname, user, port)
        self.log.raiseInfo(2, host, port, dbname)

    def closeConnect(self):
        if len(self.connection_arr) > 0:
            try:
                self.conn.close()
                for con in self.connection_arr:
                    con['conn'].close()
                self.connection_arr = []
                self.log.raiseInfo(3)
            except:
                self.log.raiseError(19)

    def get_conn(self):
        return self.conn

    def get_cur(self):
        return self.cursor

    def test_conn(self, attempt=3):
        query = """SELECT 1"""
        has_try = False
        counter_attempt = 0
        while not has_try:
            try:
                self.exec(query)
                has_try = True
            except Exception as e:
                counter_attempt += 1
                if counter_attempt <= attempt:
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