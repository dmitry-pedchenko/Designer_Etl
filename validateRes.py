
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
            self.log.logger.error(f"Error 10 - Error in exec query validate \n<{e.args[1]}>")
            self.dbService.closeConnect(self.log)
            raise SystemExit(1)


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

        self.log.logger.info('Begin validating...')

        if self.opts.args.check_mode == 'true':

            listOfNotExistInLinkedTable = []
            listOfNotExistInSourceTable = []

            for col in self.dbService.dictionary['linkedColumns']:  # нахожу все колонки которых нет в эксле линковом
                if col['linkedColName'] not in self.dbService.dataFrame_link.columns.values:
                    listOfNotExistInLinkedTable.append(col['linkedColName'])

            for col in self.dbService.dictionary['linkedColumns']:  # нахожу все колонки которые прописаны в линке
                # но их нет в сорсе
                if col['colNameInSource'] not in self.dbService.dataFrame.columns.values:
                    listOfNotExistInSourceTable.append(col['colNameInSource'])

            if len(listOfNotExistInLinkedTable) == 0 and len(listOfNotExistInSourceTable) == 0:
                for col_in_link_tag in self.dbService.dictionary['linkedColumns']:
                    for row_in_source in self.df.iterrows():
                        if row_in_source[1][col_in_link_tag['colNameInSource']] not in self.dbService.dataFrame_link[col_in_link_tag['linkedColName']].values:
                            self.log.logger.error('Error - in table <{}> value <{}> in column <{}> is not exists in column <{}> in table <{}> at list <{}>'.format(self.dbService.dictionary['importXml_path_value'],
                                                                                                                                           row_in_source[1][col_in_link_tag['colNameInSource']],
                                                                                                                                           col_in_link_tag['colNameInSource'],
                                                                                                                                           col_in_link_tag['linkedColName'],
                                                                                                                                           self.dbService.dictionary['pathToLinkFile'],
                                                                                                                                           self.dbService.dictionary['linkedFileSheetNumber'] + 1))
                            raise SystemExit(1)

                    for row_in_link in self.dbService.dataFrame_link.iterrows():
                        if row_in_link[1][col_in_link_tag['linkedColName']] not in self.dbService.dataFrame[col_in_link_tag['colNameInSource']].values:
                            self.log.logger.error('Error - in table <{}> value <{}> in column <{}> is not exists in column <{}> in table <{}> at list <{}>'.format(self.dbService.dictionary['pathToLinkFile'],
                                                                                                                                           row_in_link[1][col_in_link_tag['linkedColName']],
                                                                                                                                           col_in_link_tag['linkedColName'],
                                                                                                                                           col_in_link_tag['colNameInSource'],
                                                                                                                                           self.dbService.dictionary['importXml_path_value'],
                                                                                                                                           self.dbService.dictionary['sheetNumber_value'] + 1))
                            raise SystemExit(1)

        if self.dbService.dictionary['dictMode'] == 'true':
            counter = 1
            for col_prop in self.dbService.dictionary['dbColumns']:
                if col_prop['fromDb'] == 'true' and self.dbService.dictionary['withDict_mode'] == 'false':
                    self.log.logger.error(f'Error - In tag <exportTable> in column number <{counter}> column property <fromDb>true</fromDb> '
                                          'but <withDict mode="false">')
                    raise SystemExit(1)
                counter += 1
            counter = 0
            for col in self.dbService.dictionary['dbColumns']:
                if col['fromDb'] == 'true':
                    counter += 1
                    break
            if counter == 0:
                self.log.logger.error(
                    'Error - Mode <dict>true<dict> but in tag <dbColumns> no column property <fromDb>true</fromDb> ')
                raise SystemExit(1)
            counter = 1
            for col_in_withDict in self.dbService.dictionary['withDict']:
                if col_in_withDict['colNameDb'] == None :
                    self.log.logger.error(f"Error - In tag <withDict> in column number <{counter}> tag <colNameDb> == <None>")
                    raise SystemExit(1)
                if col_in_withDict['colName'] == None:
                    self.log.logger.error(f"Error - In tag <withDict> in column number <{counter}> tag <colName> == <None>")
                    raise SystemExit(1)
                counter += 1



        for colums_in in self.dbService.dictionary['dbColumns']:
            if colums_in['ifNull_mode'] == 'false' and colums_in['fromExcel'] == 'true':
                col_name_in_source = list(filter(lambda x: x['colNameDb'] == colums_in['colName'], self.dbService.dictionary['excelColumns']))[0]['colName']
                if 'null' in self.dbService.dataFrame[col_name_in_source].values:
                    self.log.logger.error('Error - column <{}> in file <{}> at list <{}> contains Null but column not Null'.format(col_name_in_source,
                                                                                                                  self.dbService.dictionary['importXml_path_value'],
                                                                                                                  self.dbService.dictionary['sheetNumber_value'] + 1))
                    raise SystemExit(1)

        for col in self.dic['excelColumns']:
            if col['isPK'] == 'true':
                for row in self.df[col['colName']].value_counts().to_frame().reset_index().rename(columns={'index': 'values', col['colName']:'count'}).iterrows():
                    if row[1]['count'] > 1:
                        self.log.logger.error('Error - Value <{}> in column <{}> in file <{}> at list <{}> is not unique'.format(row[1]['values']
                                                                                                                         , col['colName']
                                                                                                                         , self.dbService.dictionary['importXml_path_value']
                                                                                                                         , self.dbService.dictionary['sheetNumber_value'] + 1))
                        raise SystemExit(1)


        for column_name in db_columns:
            col_db_properties = list(filter(lambda x: x["colName"] == column_name, self.dic["dbColumns"])) # находим свойства текущей колонки
            if col_db_properties[0]["fromExcel"] == 'true' and col_db_properties[0]["isAutoInc"] == 'false':  # берем только те которые должны идти из файла
                if column_name not in excel_columns_Db_to_source:
                    listOfNotExist_db_to_source.append(column_name)

        for row in excel_columns:
            if row not in self.df.columns.values:
                self.log.logger.error("Error 11 - Column: <{}> not exists in <{}> on list <{}>. You must chose from this names: <{}>".format(row, self.dic["importXml_path_value"],self.dic['sheetNumber_value'] + 1, self.df.columns.values))
                self.dbService.closeConnect(self.log)
                raise SystemExit(1)

        columns = self.queryForColumns()

        for col in db_columns:
            if str(col) not in [i[0] for i in columns]:  # генератор потому что хранится как [('',),('',)]
                listOfNotExistInConfig.append(col)

        for col in [i[0] for i in columns]:
            if str(col) not in db_columns:
                listOfNotExistInDB.append(col)

        if len(listOfNotExistInDB) > 0:
            self.log.logger.error("Error 12 - Columns: <{}> not exists in exportTable/columns list in config".format([i for i in listOfNotExistInDB]))
            self.dbService.closeConnect(self.log)
            raise SystemExit(1)

        if len(listOfNotExistInConfig) > 0:
            self.log.logger.error(
                "Error 13 - Columns: <{}> not exists in table <{}>; In DB: <{}>".format([i for i in listOfNotExistInConfig], self.dic["exportTableName_value"], self.dic["dbBase"]))
            self.dbService.closeConnect(self.log)
            raise SystemExit(1)

        if len(listOfNotExist_db_to_source) > 0:
            self.log.logger.error(
                "Error 14 - Columns: <{}> not exists in importXml/columns/column/colNameDb tag in the <{}> file configuration. "
                "\nList of exists columns in that tag: <{}>".format(listOfNotExist_db_to_source, self.dic["importXml_path_value"], excel_columns_Db_to_source)
            )
            self.dbService.closeConnect(self.log)
            raise SystemExit(1)

        if self.opts.args.check_mode == 'true':
            if len(listOfNotExistInLinkedTable) > 0:
                self.log.logger.error(
                    "Error - Columns: <{}> not exists in linked table. "
                    "List of exists columns in that tag: <{}>".format(listOfNotExistInLinkedTable,
                                                                      self.dbService.dataFrame_link.columns.values)
                )
                self.dbService.closeConnect(self.log)
                raise SystemExit(1)

            if len(listOfNotExistInSourceTable) > 0:
                self.log.logger.error(
                    "Error - Columns: <{}> not exists in linked table. "
                    "List of exists columns in that tag: <{}>".format(listOfNotExistInSourceTable,
                                                                      self.dbService.dataFrame.columns.values)
                )
                self.dbService.closeConnect(self.log)
                raise SystemExit(1)

        self.log.logger.info('Validate success')




