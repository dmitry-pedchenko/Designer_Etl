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
        except Exception:
            log.error("Can't parse excel file")
            raise SystemExit(1)
