import rowTransformationHelper as helper
import os
import pandas as pd

class Query:
    def __init__(self, dbService, log, opts):
        self.log = log
        self.pathToLog = log.pathToNewFolder
        self.dic = dbService.dictionary
        self.DF = dbService.dataFrame
        self.cur = dbService.cursor
        self.conn = dbService.conn
        self.dbService = dbService
        self.opts = opts

    def take_df_of_dicDb(self):
        select_columns_string = ''
        list_of_columns_to_select = []

        db_table = self.dbService.dictionary['dictTableName']
        list_of_FK = [i['colName'] for i in
                      list(filter(lambda x: x['fromDb'] == 'true', self.dbService.dictionary['dbColumns']))]

        for columns in self.dbService.dictionary['withDict']:
            list_of_columns_to_select.append(columns['colNameDb'])
        for columns in list_of_FK:
            list_of_columns_to_select.append(columns)

        for columns in list_of_columns_to_select:
            select_columns_string += columns + ','

        select_columns_string = select_columns_string[:-1]

        query = f""" SELECT {select_columns_string} FROM {db_table}"""
        self.cur.execute(query)
        res = self.cur.fetchall()

        df_res = []
        for row in res:
            row_to_append = []
            for elem in row:
                if type(elem) == str:
                    row_to_append.append(elem.replace('\xa0', '\xa0').strip())
                if type(elem) == int:
                    row_to_append.append(elem)
            df_res.append(row_to_append)

        return pd.DataFrame(df_res, columns=list_of_columns_to_select)


    def createPreQuery(self, type, dicOfValsToInsert, dicOfValsUpdateCondition):
        query = ''
        tableDB = self.dic["exportTableName_value"]
        colNames = ''
        valString = ''
        whereCondition = ''

        if type == 'insert':
            for columns in dicOfValsToInsert:
                colNames += " " + columns + ","
                valString += " " + str(dicOfValsToInsert.get(columns)) + ","

            colNames = colNames[:-1]  # убираю последнюю запятую
            valString = valString[:-1]
            query = "INSERT INTO " + tableDB + " ( " + colNames + " ) VALUES " + " ( " + valString + " ); "

        if type == 'update':
            for columns in dicOfValsToInsert:
                colNames += " " + columns + " = " + str(dicOfValsToInsert.get(columns)) + ","
            for columns in dicOfValsUpdateCondition:
                whereCondition += " " + columns + " = " + str(dicOfValsUpdateCondition.get(columns)) + ","

            colNames = colNames[:-1]  # убираю последнюю запятую
            whereCondition = whereCondition[:-1]  # убираю последнюю запятую
            query = "UPDATE " + tableDB + " SET " + colNames + " WHERE " + whereCondition

        return query

    def execQuery(self, query):
        if self.dic["testRunMode_value"] == 'true':
            self.log.raiseDebug(0, query)
            self.rowCounter += 1
        elif self.dic["testRunMode_value"] == 'false':
            try:
                self.cur.execute(query)
                self.conn.commit()
                self.counter += 1
            except Exception as e:
                self.log.raiseDebug(1, self.rowCounter + 2, query, e.args[1])
                # не прерываем идем дальше если выкинуло исключение только логиним
            finally:
                self.rowCounter += 1
        else:
            self.dbService.closeConnect(self.log)
            self.log.raiseError(34)

    def execAllQueries(self):
        self.log.raiseInfo(8)
        self.log.raiseInfo(9,self.dic["testRunMode_value"])
        self.counter = 0    # при каждом запуске скрипта обнуляем счетчик успешно всятавленных строк
        self.rowCounter = 0 # при каждом запуске скрипта обнуляем счетчик общего количества строк
        arrOfSourceColumns = []
        dicOfColVals = {}
        dicOfValsToInsert = {}
        dicOfValsUpdateCondition = {}
        arrOfLoadPercents = [25, 50, 75, 100]

        hp = helper.transformHelper()

        for each in self.dic["excelColumns"]:

            arrOfSourceColumns.append({"colNameDb":each["colNameDb"],"colName":each["colName"]})  # собираю массив из колонок которые надо брать

        if self.dbService.dictionary['dictMode'] == 'true':
            self.take_df_of_dicDb()

        for row in self.DF.iterrows():

            for each in arrOfSourceColumns:  # прохожу по столбцам в источнике и собираю словарь значений и колонок
                # с именами ключей в виде названия колонки в приемнике
                dicOfColVals[each["colNameDb"]] = []  # список потому что может быть несколько полей
                dicOfColVals[each["colNameDb"]].append(row[1][each["colName"]])

            for columnProperty in self.dic["dbColumns"]:      # прохожу по колонкам в базе данных

                if columnProperty["isAutoInc"] == 'true':
                    continue # поля с автоинкрементом не берем а идем дальше и не вносим их в список

                curColumnExcelEqualsDbColumn = list(filter(lambda x: x["colNameDb"] == columnProperty["colName"], self.dic["excelColumns"]))

                # надо пройтись по значениям dicOfColVals и развернуть список
                
                if dicOfColVals.get(columnProperty["colName"]) != None:  # беру имя колонки в базе и
                                                                 # смотрю есть ли оно в списке источника
                    if columnProperty.get("colType") == 'str' and dicOfColVals.get(columnProperty["colName"]) != 'null': #
                        dicOfValsToInsert[columnProperty["colName"]] = " '{}' ".format(hp.checkAndTransform(columnProperty, curColumnExcelEqualsDbColumn[0], dicOfColVals.get(columnProperty["colName"])))
                    else:
                        dicOfValsToInsert[columnProperty["colName"]] = hp.checkAndTransform(columnProperty, curColumnExcelEqualsDbColumn[0],dicOfColVals.get(columnProperty["colName"]))

                elif columnProperty['defaultValue_mode'] == 'true':
                    # если нет такой колонки в файле беру из дефолтного поля
                    if columnProperty.get("colType") == 'str':
                        dicOfValsToInsert[columnProperty["colName"]] = " '{}' ".format(columnProperty["defaultValue"])
                    else:
                        dicOfValsToInsert[columnProperty["colName"]] = columnProperty["defaultValue"]

                elif columnProperty['fromDb'] == 'true':
                    FK = [i['colName'] for i in
                                  list(filter(lambda x: x['fromDb'] == 'true', self.dbService.dictionary['dbColumns']))][0]
                    df_dic = self.take_df_of_dicDb()
                    df_start = df_dic[self.dbService.dictionary['withDict'][0]['colNameDb']] == row[1][self.dbService.dictionary['withDict'][0]['colNameDb']]
                    for col in self.dbService.dictionary['withDict']:
                        df_c = df_dic[col['colNameDb']] == hp.checkAndTransform(columnProperty, col,value=row[1][col['colNameDb']]).strip()
                        df_start = df_c & df_start
                    index = None
                    for i in df_dic.loc[df_start].iterrows():
                        index = i[1][FK]
                    dicOfValsToInsert[columnProperty["colName"]] = index

            if self.dbService.dictionary['loadMode'] == 'update':
                arrOfUpdatedCondionInDbColumns = [i['colName'] for i in list(filter(lambda x: x['isUpdateCondition'] == 'true', self.dbService.dictionary['dbColumns']))]
                for key in arrOfUpdatedCondionInDbColumns:
                    dicOfValsUpdateCondition[key] = dicOfValsToInsert.get(key)
                    dicOfValsToInsert.pop(key)

            if self.rowCounter == 0:
                self.log.raiseInfo(10, 0)
            if ((100 * self.rowCounter) / len(self.DF)) > arrOfLoadPercents[0]:
                self.log.raiseInfo(10, arrOfLoadPercents[0])
                arrOfLoadPercents.pop(0)
            if self.rowCounter == len(self.DF):
                self.log.raiseInfo(10, arrOfLoadPercents[0])

            fullQuery = self.createPreQuery(self.dbService.dictionary['loadMode'], dicOfValsToInsert,dicOfValsUpdateCondition)
            self.execQuery(fullQuery)

        if self.dic["testRunMode_value"] == 'true':
            self.log.raiseInfo(11, self.rowCounter)
            self.log.raiseInfo(13, self.pathToLog)
        else:
            self.log.raiseInfo(12, self.counter, self.rowCounter - self.counter)
            self.log.raiseInfo(13, self.pathToLog)
