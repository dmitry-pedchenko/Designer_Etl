
class Transformation_helper:

    def cropEnd(self, value, valueToCrop):
        return str(value)[:-int(valueToCrop)]
    def addValueEnd(self, value, valueToAdd):
        return "{}{}".format(value, valueToAdd)
    def takeFromBegin(self,value , transformValue):
        if value is not None:
            return str(value)[0:int(transformValue)]
    def cropBegin(self, value, transformValue):
        return str(value)[int(transformValue):]
    def addValueBegin(self, value, valueToAdd):
        return "{}{}".format(valueToAdd, value)
    def addValueBoth(self, value, valToBegin, valToEnd):
        return "{}{}{}".format(valToBegin, value, valToEnd)
    def replace(self, value, replaceValArr):
        for row in replaceValArr:
            repToVal = row["replaceToValue"]

            if row["replaceValue"] == str(value):
                return repToVal
        return value

    def checkAndTransform(self, dbProperties = None, rowProperties = None, value = None, str_type = None):
        self.value = value
        if rowProperties.get("cropEnd_mode") == 'true':
            self.value = self.cropEnd(self.value, rowProperties.get("cropEnd"))
        if rowProperties.get("cropBegin_mode") == 'true':
            self.value = self.cropBegin(self.value, rowProperties.get("cropBegin"))
        if rowProperties.get("addValueEnd_mode") == 'true':
            self.value = self.addValueEnd(self.value, rowProperties.get("addValueEnd"))
        if rowProperties.get("takeFromBegin_mode") == 'true':
            self.value = self.takeFromBegin(self.value, rowProperties.get("takeFromBegin"))
        if rowProperties.get("addValueBegin_mode") == 'true':
            self.value = self.addValueBegin(self.value, rowProperties.get("addValueBegin"))
        if rowProperties.get("addValueBoth_mode") == 'true':
            self.value = self.addValueBoth(self.value, rowProperties.get("addValueBoth").split(',')[0],
                                                        rowProperties.get("addValueBoth").split(',')[1])
        if rowProperties.get("replace_mode") == 'true':
            self.value = self.replace(self.value, rowProperties.get("replaceValArr"))

        if dbProperties:
            if dbProperties.get("ifNull_mode") == 'true' and value == 'null':
                self.value = dbProperties.get("ifNull")
        if str_type == 'date':
            self.value = value.strftime("%Y%m%d")
            return self.value

        return str(self.value).replace('\n', '').replace("'", "''").strip()
