import pandas as pd



class ExcelSelect:

    def __init__(self, path, listNumber, log, arrOfColTypesInExcel):
        arrConverters = {}

        lambdaStr = lambda x: str(x)
        lambdaInt = lambda x: int(x)
        lambdaFloat = lambda x: float(x)

        for col in arrOfColTypesInExcel.keys():
            if arrOfColTypesInExcel.get(col) == 'str':
                arrConverters[col] = lambdaStr
            if arrOfColTypesInExcel.get(col) == 'int':
                arrConverters[col] = lambdaInt
            if arrOfColTypesInExcel.get(col) == 'float':
                arrConverters[col] = lambdaFloat

        try:
            df = pd.ExcelFile(path)
            sheet = df.parse(listNumber, converters=arrConverters)
            self.sheet_name = df.sheet_names[listNumber]
            self.newDf = sheet.fillna("null")
        except Exception as e:
            log.raiseError(35, e.args[0])
            raise SystemExit(1)

class Dic_DF:
    __instance = None
    dic_of_df = {'query': None, 'data_frame': None}

    @classmethod
    def get_instance(cls, log):
        if not cls.__instance:
            cls.__instance = Dic_DF(log)
        return cls.__instance

    def __init__(self, log):
        self.log = log

    def take_df_of_dicDb(self, cur, dbService, connector):
        select_columns_string = ''
        list_of_columns_to_select = []

        db_table = dbService.dictionary['dictTableName']
        list_of_FK = [i['colName'] for i in
                      list(filter(lambda x: x['fromDb'] == 'true', dbService.dictionary['dbColumns']))]

        for columns in dbService.dictionary['withDict']:
            list_of_columns_to_select.append(columns['colNameDb'])
        for columns in list_of_FK:
            list_of_columns_to_select.append(columns)

        for columns in list_of_columns_to_select:
            select_columns_string += columns + ','

        select_columns_string = select_columns_string[:-1]

        query = f""" SELECT {select_columns_string} FROM {db_table}"""

        if self.dic_of_df.get('query') != query or self.dic_of_df.get('query') is None:
            self.dic_of_df['query'] = query
            connector.test_conn(3)
            try:
                cur.execute(query)
                res = cur.fetchall()
            except Exception as e:
                self.log.raiseError(38, e.args[1])

            df_res = []
            for row in res:
                row_to_append = []
                for elem in row:
                    if type(elem) == str:
                        row_to_append.append(elem.replace('\xa0', '\xa0').strip())
                    if type(elem) == int:
                        row_to_append.append(elem)
                df_res.append(row_to_append)
            self.dic_of_df['data_frame'] = pd.DataFrame(df_res, columns=list_of_columns_to_select)
            return self.dic_of_df['data_frame']
        else:
            return self.dic_of_df['data_frame']
