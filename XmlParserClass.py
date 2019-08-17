import pymssql as p
import xmlParser
import DAO
import os




class XmlParser:

    def __init__(self, pathToConfig, log, opts):
        try:
            self.dictionary = xmlParser.xmlParse(pathToConfig, log, opts)
        except Exception as e:
            log.logger.error("Error 1 - Error at parsing XML configuration file", e)
            raise SystemExit(1)
        pathToExcel = os.path.join(os.path.join(os.getcwd(), 'source'), self.dictionary["importXml_path_value"])
        if opts.args.check_mode == 'true':
            pathToExcel_link = os.path.join(os.path.join(os.getcwd(), 'source'), self.dictionary["pathToLinkFile"])

        arrOfColTypesInExcel = {}
        for prop in self.dictionary["excelColumns"]:
            arrOfColTypesInExcel[prop['colName']] = prop['colType']


        try:
            dao = DAO.ExcelSelect(pathToExcel, self.dictionary["sheetNumber_value"], log, arrOfColTypesInExcel)
            self.dataFrame = dao.newDf

            log.logger.info("Success excel file: <{}> opened on page name: <{}>, list number: <{}>".format(self.dictionary["importXml_path_value"],
                                                                                                     dao.sheet_name, self.dictionary["sheetNumber_value"] + 1))
        except Exception as e:
            log.logger.error("Error 8 - Can't open Excel path: <{}> on page: <{}> - <{}>".format(self.dictionary["importXml_path_value"],
                                                                                      int(self.dictionary["sheetNumber_value"]) + 1, e.args[0]))
            raise SystemExit(1)

        if opts.args.check_mode == 'true':  # собираю массив свйоств и имен клонок для связанной таблицы --check_mode
            arrOfColTypesInExcelLinked = {}
            for prop in self.dictionary["linkedColumns"]:
                try:
                    arrOfColTypesInExcelLinked[prop['linkedColName']] = list(filter(lambda x: x['colName'] ==
                                                                                              prop['colNameInSource'],
                                                                                    self.dictionary['excelColumns']))[0]['colType']
                except:
                    log.logger.error("Error - Can't find <colName> for <colNameInSource> ")
                    raise SystemExit(1)

        try:
            if opts.args.check_mode == 'true':
                dao_link = DAO.ExcelSelect(pathToExcel_link, self.dictionary["linkedFileSheetNumber"], log, arrOfColTypesInExcelLinked)
                self.dataFrame_link = dao_link.newDf
        except Exception as e:
            log.logger.error(
                "Error 8 - Can't open Excel path: <{}> on page: <{}> - <{}>".format(self.dictionary["pathToLinkFile"],
                                                                         int(self.dictionary["linkedFileSheetNumber"]) + 1, e.args[0]))
            raise SystemExit(1)

    def connectToTheDB(self, log):
        host = self.dictionary["dbHost"]
        user = self.dictionary["dbUser"]
        password = self.dictionary["dbPass"]
        dbname = self.dictionary["dbBase"]
        port = self.dictionary["dbPort"]

        try:
            self.conn = p.connect(host=host, port=port, user=user, password=password, database=dbname)
            self.cursor = self.conn.cursor()
        except Exception as e:
            log.logger.error("Error 9 - Fail to connect to <{}> <{}> <{}> <{}>".format(host, dbname, user, port))
            raise SystemExit(1)
        log.logger.info("Success connection to host: {0}, port: {2}, database name: {1}".format(host, dbname,
                                                                                             port))

    def closeConnect(self, log):
        try:
            self.conn.close()
            log.logger.info("Connection to DB closed")
        except Exception as e:
            log.logger.error("Fail to close connection")




