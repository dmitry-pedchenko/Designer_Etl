from Core.Validate import Row_transformation_helper as helper
from Core.DAO.DAO_DataFrame import Dic_DF as df
from Core.Validate.Filter import filter_arr


class Query:
    def __init__(self, dbService, log, opts, connector):
        self.connector = connector
        self.log = log
        self.pathToLog = log.pathToNewFolder
        self.dic = dbService.dictionary
        self.DF = dbService.dataFrame
        self.cur = connector.get_cur()
        self.conn = connector.get_conn()
        self.dbService = dbService
        self.opts = opts

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
            self.connector.test_conn(3)
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
            self.connector.closeConnect()
            self.log.raiseError(34)

    def execAllQueries(self):
        self.log.raiseInfo(8)
        self.log.raiseInfo(9,self.dic["testRunMode_value"])
        self.counter = 0    # при каждом запуске скрипта обнуляем счетчик успешно всятавленных строк
        self.rowCounter = 0 # при каждом запуске скрипта обнуляем счетчик общего количества строк
        arrOfSourceColumns = []
        dicOfColVals = {}   # словарь с именами полей и значениями полей из экселя
        dicOfValsToInsert = {} # словарь со всеми значениями которые нужно вставить в приемник
        dicOfValsUpdateCondition = {} # словарь со значениями для вставки в режиме обновления
        arrOfLoadPercents = [25, 50, 75, 100]


        hp = helper.Transformation_helper()

        for each in self.dic["excelColumns"]:
            # собираю массив из колонок которые надо брать
            arrOfSourceColumns.append({"colNameDb": each["colNameDb"], "colName": each["colName"]})

        if self.dbService.dictionary['dictMode'] == 'true':
            df_of_dic = df.get_instance(self.log)
            df_of_dic.clear()  # очищаю датафреймы со словарями чтобы на след загрузке были с новыми данными
        for row in self.DF.iterrows():
            filter_flag_arr = []  # флаг указывающий на то что фильтр сработал и в строке неподходящее значение
            post_filter_flag_arr = []  # флаг указывающий на то что пост фильтр сработал и в строке неподходящее значение
            for each in arrOfSourceColumns:
                if list(filter(lambda x: x["colName"] == each["colName"], self.dic["excelColumns"]))[0]['filter_mode'] == 'true':
                    filter_flag_arr.append(
                        filter_arr(self.log,
                                   list(filter(lambda x: x["colName"] == each["colName"], self.dic["excelColumns"]))[0]['colType'],
                                   list(filter(lambda x: x["colName"] == each["colName"], self.dic["excelColumns"]))[0]['filterArr'],
                                   hp.checkAndTransform(rowProperties=list(filter(lambda x: x["colName"] == each["colName"], self.dic["excelColumns"]))[0],
                                                        value=row[1][each["colName"]],
                                                        str_type=list(filter(lambda x: x["colName"] == each["colName"], self.dic["excelColumns"]))[0]['colType'])
                                   ))

                if list(filter(lambda x: x["colName"] == each["colName"], self.dic["excelColumns"]))[0]['post_filter_mode'] == 'true':
                    post_filter_flag_arr.append(
                        filter_arr(self.log,
                                   list(filter(lambda x: x["colName"] == each["colName"], self.dic["excelColumns"]))[0]['colType'],
                                   list(filter(lambda x: x["colName"] == each["colName"], self.dic["excelColumns"]))[0]['postfilterArr'],
                                   hp.checkAndTransform(rowProperties=list(filter(lambda x: x["colName"] == each["colName"], self.dic["excelColumns"]))[0],
                                                        value=row[1][each["colName"]],
                                                        str_type=list(filter(lambda x: x["colName"] == each["colName"], self.dic["excelColumns"]))[0]['colType'])
                                   ))
                # прохожу по столбцам в источнике и собираю словарь значений и колонок
                # с именами ключей в виде названия колонки в приемнике
                # список потому что может быть несколько полей
                if dicOfColVals.get(each["colNameDb"]) is None:
                    #  если в списке нет значения для данного поля
                    dicOfColVals[each["colNameDb"]] = []
                    dicOfColVals[each["colNameDb"]].append(row[1][each["colName"]])
                else:
                    dicOfColVals[each["colNameDb"]].append(row[1][each["colName"]])
            if False in filter_flag_arr:
                # если есть значение которое попало под фильтр то пропускаем эту строчку
                dicOfColVals = {}
                continue

            if False in post_filter_flag_arr:
                # если есть значение которое попало под пост фильтр то пропускаем эту строчку
                dicOfColVals = {}
                continue

            for columnProperty in self.dic["dbColumns"]:      # прохожу по колонкам в базе данных

                if columnProperty["isAutoInc"] == 'true':
                    continue  # поля с автоинкрементом не берем а идем дальше и не вносим их в список

                curColumnExcelEqualsDbColumn = list(filter(lambda x: x["colNameDb"] == columnProperty["colName"], self.dic["excelColumns"]))

                # надо пройтись по значениям dicOfColVals и развернуть список

                if dicOfColVals.get(columnProperty["colName"]) is not None:
                                                                # беру имя колонки в базе и
                                                                 # смотрю есть ли оно в списке источника
                    if len(dicOfColVals.get(columnProperty["colName"])) == 1:
                        # если на одно поле в приемнике одно поле в источнике
                        if columnProperty.get("colType") == 'str' and dicOfColVals.get(columnProperty["colName"])[0] != 'null':
                            dicOfValsToInsert[columnProperty["colName"]] = " '{}' ".format(hp.checkAndTransform(columnProperty,
                                                                                                                curColumnExcelEqualsDbColumn[0],
                                                                                                                dicOfColVals.get(columnProperty["colName"])[0],
                                                                                                                str_type=curColumnExcelEqualsDbColumn[0]['colType']))
                        elif columnProperty.get("colType") == 'int':
                            dicOfValsToInsert[columnProperty["colName"]] = hp.checkAndTransform(columnProperty,
                                                                                                curColumnExcelEqualsDbColumn[0],
                                                                                                dicOfColVals.get(columnProperty["colName"])[0],
                                                                                                str_type=curColumnExcelEqualsDbColumn[0]['colType'])
                        else:
                            if columnProperty.get('ifNull') in ['null', 'Null', 'NULL']:
                                dicOfValsToInsert[columnProperty["colName"]] = hp.checkAndTransform(columnProperty,
                                                                                                    curColumnExcelEqualsDbColumn[0],
                                                                                                    dicOfColVals.get(columnProperty["colName"])[0],
                                                                                                    str_type=curColumnExcelEqualsDbColumn[0]['colType'])
                            else:
                                dicOfValsToInsert[columnProperty["colName"]] = " '{}' ".format(hp.checkAndTransform(columnProperty,
                                                                                                                    curColumnExcelEqualsDbColumn[0],
                                                                                                                    dicOfColVals.get(columnProperty["colName"])[0],
                                                                                                                    str_type=curColumnExcelEqualsDbColumn[0]['colType']))
                    else:  # если несколько полей в источнике идут в одно поле в приемнике
                        if columnProperty.get("colType") == 'str':  #
                            string = ''
                            for number, col in enumerate(dicOfColVals.get(columnProperty["colName"])):
                                columnProperty_for_conc = list(filter(lambda x: x['colNameDb'] == columnProperty["colName"], self.dic["excelColumns"]))[number]
                                string += "{}".format(hp.checkAndTransform(rowProperties=columnProperty_for_conc,
                                                                           dbProperties=columnProperty,
                                                                           value=col,
                                                                           str_type=columnProperty_for_conc['colType']))
                            string = f"'{string}'"
                            dicOfValsToInsert[columnProperty["colName"]] = string
                        else:
                            self.log.raiseError(36)

                elif columnProperty['defaultValue_mode'] == 'true':
                    # если нет такой колонки в файле беру из дефолтного поля
                    if columnProperty.get("colType") == 'str':
                        dicOfValsToInsert[columnProperty["colName"]] = " '{}' ".format(columnProperty["defaultValue"])
                    else:
                        dicOfValsToInsert[columnProperty["colName"]] = columnProperty["defaultValue"]

                elif columnProperty['fromDb'] == 'true':
                    FK = columnProperty['colName']
                    df_dic = df_of_dic.take_df_of_dicDb(self.cur, self.dbService, self.connector, FK)
                    cur_table = list(filter(lambda x: x["indxDbColumn"] == FK, self.dbService.dictionary['withDict']))[0]

                    try:
                        df_start = df_dic[f"""{cur_table['arrOfDictColumns'][0]['colNameDb']}"""] \
                                   == f"""{row[1][cur_table['arrOfDictColumns'][0]['colName']]}"""
                    except Exception as e:
                        self.log.raiseError(39, e.args[0])
                    for num, col in enumerate(cur_table['arrOfDictColumns']):
                        df_c = df_dic[col['colNameDb']] == hp.checkAndTransform(columnProperty,
                                                                                col,
                                                                                value=row[1][col['colName']],
                                                                                str_type=cur_table['arrOfDictColumns'][num]['colType'])
                        df_start = df_c & df_start
                    index = None
                    for i in df_dic.loc[df_start].iterrows():
                        index = i[1][cur_table['indxColumnDic']]
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
            if self.rowCounter == len(self.DF) - 1:
                self.log.raiseInfo(10, arrOfLoadPercents[0])

            fullQuery = self.createPreQuery(self.dbService.dictionary['loadMode'], dicOfValsToInsert, dicOfValsUpdateCondition)
            self.execQuery(fullQuery)

            dicOfColVals = {}  # очищаю словарь чтобы на следующей итерации снова начал заполняться

        if self.dic["testRunMode_value"] == 'true':
            self.log.raiseInfo(11, self.rowCounter)
            self.log.raiseInfo(13, self.pathToLog)
        else:

            if not self.log.debug_stat_dict:
                pass
            else:
                self.log.raiseDebug(0, "\n\nDEBUG OVERALL\n")
                for debug in self.log.debug_stat_dict:
                    self.log.raiseDebug(0, f"\n\n -----------------\nDEBUG MESSAGE FROM DATABSE\n\n"
                                           f"{debug}\n\n"
                                           f"NUMBER OF ENTRIES :\n {self.log.debug_stat_dict.get(debug)}\n"
                                           f"-----------------\n")

                self.log.clear_debug()

            self.log.raiseInfo(12, self.counter, self.rowCounter - self.counter)
            self.log.raiseInfo(13, self.pathToLog)



