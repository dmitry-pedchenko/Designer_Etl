
class Validate:
    def __init__(self, dbService, log, opts):
        self.dic = dbService.dictionary
        self.df = dbService.dataFrame
        self.log = log
        self.cur = dbService.cursor
        self.conn = dbService.conn
        self.dbService = dbService
        self.opts = opts

        if opts.args.check_mode == 'true':
            self.df_link = dbService.dataFrame_link

    def execSelect(self, query):
        try:
            self.cur.execute(query)
            return self.cur.fetchall()
        except Exception as e:
            self.log.raiseError(20, e.args[1])
            self.dbService.closeConnect(self.log)

    def queryForColumns(self):
        query = f""" SELECT name FROM syscolumns c WHERE c.id = OBJECT_ID('{self.dic["exportTableName_value"]}'); """
        return self.execSelect(query)


    def validate(self):
        excel_columns = [i["colName"] for i in self.dic["excelColumns"]]
        excel_columns_Db_to_source = [i["colNameDb"] for i in self.dic["excelColumns"]]
        db_columns = [i["colName"] for i in self.dic["dbColumns"]]

        listOfNotExistInDB = []
        listOfNotExistInConfig = []
        listOfNotExist_db_to_source = []

        self.log.raiseInfo(5)

        if self.opts.args.check_mode == 'true':

            listOfNotExistInLinkedTable = []
            listOfNotExistInSourceTable = []

            # нахожу все колонки которых нет в эксле линковом
            for col in self.dbService.dictionary['linkedColumns']:
                if col['linkedColName'] not in self.dbService.dataFrame_link.columns.values:
                    listOfNotExistInLinkedTable.append(col['linkedColName'])

            # нахожу все колонки которые прописаны в линке но их нет в сорсе
            for col in self.dbService.dictionary['linkedColumns']:
                if col['colNameInSource'] not in self.dbService.dataFrame.columns.values:
                    listOfNotExistInSourceTable.append(col['colNameInSource'])

            if len(listOfNotExistInLinkedTable) == 0 and len(listOfNotExistInSourceTable) == 0:
                for col_in_link_tag in self.dbService.dictionary['linkedColumns']:
                    for row_in_source in self.df.iterrows():
                        if row_in_source[1][col_in_link_tag['colNameInSource']] not in self.dbService.dataFrame_link[col_in_link_tag['linkedColName']].values:
                            self.log.raiseError(21,self.dbService.dictionary['importXml_path_value'],
                                                row_in_source[1][col_in_link_tag['colNameInSource']],
                                                col_in_link_tag['colNameInSource'],
                                                col_in_link_tag['linkedColName'],
                                                self.dbService.dictionary['pathToLinkFile'],
                                                self.dbService.dictionary['linkedFileSheetNumber'] + 1)
                            

                    for row_in_link in self.dbService.dataFrame_link.iterrows():
                        if row_in_link[1][col_in_link_tag['linkedColName']] not in self.dbService.dataFrame[col_in_link_tag['colNameInSource']].values:
                            self.log.raiseError(21,self.dbService.dictionary['pathToLinkFile'],
                                               row_in_link[1][col_in_link_tag['linkedColName']],
                                               col_in_link_tag['linkedColName'],
                                               col_in_link_tag['colNameInSource'],
                                               self.dbService.dictionary['importXml_path_value'],
                                               self.dbService.dictionary['sheetNumber_value'] + 1)

        if self.dbService.dictionary['dictMode'] == 'true':

            for counter, col_prop in enumerate(self.dbService.dictionary['dbColumns'], 1):
                if col_prop['fromDb'] == 'true' and self.dbService.dictionary['withDict_mode'] == 'false':
                    self.log.raiseError(22, counter)
            counter_fromDb = 0
            for col in self.dbService.dictionary['dbColumns']:
                if col['fromDb'] == 'true':
                    counter_fromDb += 1
                    break
            if counter_fromDb == 0:
                self.log.raiseError(23)

            for counter, col_in_withDict in enumerate(self.dbService.dictionary['withDict'], 1):
                if col_in_withDict['colNameDb'] == None :
                    self.log.raiseError(24, counter)
                    
                if col_in_withDict['colName'] == None:
                    self.log.raiseError(25, counter)


        for colums_in in self.dbService.dictionary['dbColumns']:
            if colums_in['ifNull_mode'] == 'false' and colums_in['fromExcel'] == 'true':
                col_name_in_source = list(filter(lambda x: x['colNameDb'] == colums_in['colName'], self.dbService.dictionary['excelColumns']))[0]['colName']
                if 'null' in self.dbService.dataFrame[col_name_in_source].values:
                    self.log.raiseError(26,col_name_in_source,self.dbService.dictionary['importXml_path_value'],
                                                            self.dbService.dictionary['sheetNumber_value'] + 1)

        for col in self.dic['excelColumns']:
            if col['isPK'] == 'true':
                for row in self.df[col['colName']].value_counts().to_frame().reset_index().rename(columns={'index': 'values', col['colName']:'count'}).iterrows():
                    if row[1]['count'] > 1:
                        self.log.raiseError(27, row[1]['values'], col['colName'], self.dbService.dictionary['importXml_path_value']
                                                                , self.dbService.dictionary['sheetNumber_value'] + 1)

        for column_name in db_columns:
            col_db_properties = list(filter(lambda x: x["colName"] == column_name, self.dic["dbColumns"])) # находим свойства текущей колонки
            if col_db_properties[0]["fromExcel"] == 'true' and col_db_properties[0]["isAutoInc"] == 'false':  # берем только те которые должны идти из файла
                if column_name not in excel_columns_Db_to_source:
                    listOfNotExist_db_to_source.append(column_name)

        for row in excel_columns:
            if row not in self.df.columns.values:
                self.log.raiseError(28, row, self.dic["importXml_path_value"], self.dic['sheetNumber_value'] + 1, self.df.columns.values)
                self.dbService.closeConnect(self.log)

        columns = self.queryForColumns()
        for col in db_columns:
            if str(col) not in [i[0] for i in columns]:  # генератор потому что хранится как [('',),('',)]
                listOfNotExistInConfig.append(col)
        for col in [i[0] for i in columns]:
            if str(col) not in db_columns:
                listOfNotExistInDB.append(col)
        if len(listOfNotExistInDB) > 0:
            self.log.raiseError(29, [i for i in listOfNotExistInDB])
            self.dbService.closeConnect(self.log)

        if len(listOfNotExistInConfig) > 0:
            self.log.raiseError(30, [i for i in listOfNotExistInConfig], self.dic["exportTableName_value"], self.dic["dbBase"])
            self.dbService.closeConnect(self.log)

        if len(listOfNotExist_db_to_source) > 0:
            self.log.raiseError(31, listOfNotExist_db_to_source, self.dic["importXml_path_value"], excel_columns_Db_to_source)
            self.dbService.closeConnect(self.log)

        if self.opts.args.check_mode == 'true':
            if len(listOfNotExistInLinkedTable) > 0:
                self.log.raiseError(32, listOfNotExistInLinkedTable, self.dbService.dataFrame_link.columns.values)
                self.dbService.closeConnect(self.log)

            if len(listOfNotExistInSourceTable) > 0:
                self.log.raiseError(33, listOfNotExistInSourceTable, self.dbService.dataFrame.columns.values)
                self.dbService.closeConnect(self.log)

        self.log.raiseInfo(6)




