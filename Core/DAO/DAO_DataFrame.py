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
        except:
            log.raiseError(43, path)

        if not df.sheet_names:
            log.raiseError(42)

        sheet = df.parse(listNumber, converters=arrConverters)
        self.sheet_name = df.sheet_names[listNumber]
        self.newDf = sheet.fillna("null")

class Dic_DF:
    __instance = None
    dic_of_df = []

    @classmethod
    def get_instance(cls, log):
        if not cls.__instance:
            cls.__instance = Dic_DF(log)
        return cls.__instance

    def __init__(self, log):
        self.log = log

    def take_df_of_dicDb(self, cur, dbService, connector, fk):
        select_columns_string = ''
        list_of_columns_to_select = []
        db_table = list(filter(lambda x: x["indxDbColumn"] == fk, dbService.dictionary['withDict']))[0]

        for columns in db_table['arrOfDictColumns']:
            list_of_columns_to_select.append(columns['colNameDb'])

        list_of_columns_to_select.append(db_table['indxColumnDic'])

        for columns in list_of_columns_to_select:
            select_columns_string += columns + ','

        select_columns_string = select_columns_string[:-1]

        query = f""" SELECT {select_columns_string} FROM {db_table['dictTableName']}"""

        if len(self.dic_of_df) > 0:
            q_in_list = list([i.get('query') for i in self.dic_of_df])
        else:
            q_in_list = []

        if query not in q_in_list or len(self.dic_of_df) == 0:
            loc_dic = {}
            loc_dic['query'] = query
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

            loc_dic['data_frame'] = pd.DataFrame(df_res, columns=list_of_columns_to_select)

            self.dic_of_df.append(loc_dic)
            return loc_dic['data_frame']
        else:
            return list(filter(lambda x: x.get('query') == query, self.dic_of_df))[0]['data_frame']

    def clear(self):
        self.dic_of_df = []
