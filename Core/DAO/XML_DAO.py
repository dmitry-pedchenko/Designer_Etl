from Parser import XML_parser
from Core.DAO import DAO_DataFrame
import os

class XmlParser:

    def __init__(self, pathToConfig, log, opts=None):
        try:
            self.dictionary = XML_parser.do_XML_parse(pathToConfig, log, opts)
        except Exception as e:
            log.raiseError(1, e)

        pathToExcel = os.path.join(os.path.join(os.getcwd(), '..', 'Source'), self.dictionary["importXml_path_value"])
        if self.dictionary['checkMode_value'] == 'true':
            pathToExcel_link = os.path.join(os.path.join(os.getcwd(), '..', 'Source'), self.dictionary["pathToLinkFile"])

        arrOfColTypesInExcel = {}

        if self.dictionary["dictMode"] == 'false':
            for prop in self.dictionary["excelColumns"]:
                arrOfColTypesInExcel[prop['colName']] = prop['colType']
        elif self.dictionary["dictMode"] == 'true':
            for prop in self.dictionary["excelColumns"]:
                arrOfColTypesInExcel[prop['colName']] = prop['colType']
            for table in self.dictionary['withDict']:
                for prop in table['arrOfDictColumns']:
                    arrOfColTypesInExcel[prop['colName']] = prop['colType']
        try:
            dao = DAO_DataFrame.ExcelSelect(pathToExcel, self.dictionary["sheetNumber_value"], log, arrOfColTypesInExcel)
            self.dataFrame = dao.newDf
            self.df = dao.df

            log.raiseInfo(1, self.dictionary["importXml_path_value"], dao.sheet_name, self.dictionary["sheetNumber_value"] + 1)
        except Exception as e:
            log.raiseError(16, self.dictionary["importXml_path_value"], int(self.dictionary["sheetNumber_value"]) + 1, e.args[0])

        if self.dictionary['checkMode_value'] == 'true':
            # собираю массив свйоств и имен клонок для связанной таблицы checkMode
            arrOfColTypesInExcelLinked = {}
            for prop in self.dictionary["linkedColumns"]:
                try:
                    arrOfColTypesInExcelLinked[prop['linkedColName']] = \
                        list(filter(lambda x: x['colName'] == prop['colNameInSource'], self.dictionary['excelColumns']))[0]['colType']
                except:
                    log.raiseError(17)

        try:
            if self.dictionary['checkMode_value'] == 'true':
                dao_link = DAO_DataFrame.ExcelSelect(pathToExcel_link,
                                                     self.dictionary["linkedFileSheetNumber"],
                                                     log,
                                                     arrOfColTypesInExcelLinked)
                self.dataFrame_link = dao_link.newDf
                self.df_link = dao_link.df
        except Exception as e:
            log.raiseError(16,
                           self.dictionary["pathToLinkFile"],
                           int(self.dictionary["linkedFileSheetNumber"]) + 1,
                           e.args[0])
