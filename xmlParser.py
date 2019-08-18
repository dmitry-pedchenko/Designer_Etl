import xml.etree.ElementTree as et
import os


def xmlParse(pathToFile, log, opts):
    colArrayExcel = []  # массив включающий в себя все колонки из источника
    importDict = {}  # словарь для каждой колонки
    colArrayDB = []  # массив с колонками в базе

    pathToFile = os.path.join(os.path.join(os.getcwd(), 'config'), pathToFile)

    try:
        root = et.parse(pathToFile).getroot()
    except Exception as e:
        log.raiseError(2, pathToFile, e.args[0])

    try:
        sheetNumber_value = int(root.find("importXml/sheetNumber").text) - 1
    except:
        log.raiseError(3,"importXml/sheetNumber")

    try:
        testRunMode_value = opts.args.test_mode
    except:
        log.raiseError(4,"test_mode")

    try:
        dictMode= root.find("dict").text
    except:
        log.raiseError(3,"dict")

    try:
        loadMode= root.find("loadMode").text
    except:
        log.raiseError(3,"loadMode")

    try:
        checkMode_value = opts.args.check_mode
    except:
        log.raiseError(4, "check_mode")

    try:
        importXml_path_value = root.find("importXml/path").text
    except:
        log.raiseError(3, "importXml/path")

    try:
        exportTableName_value = root.find("exportTable/path").text
    except:
        log.raiseError(3, "exportTable/path")

    try:
        dbHost = root.find("dbHost").text
    except:
        log.raiseError(3, "dbHost")

    try:
        dbUser = root.find("dbUser").text
    except:
        log.raiseError(3, "dbUser")

    try:
        dbPass = root.find("dbPass").text
    except:
        log.raiseError(3, "dbPass")

    try:
        dbBase = root.find("dbBase").text
    except:
        log.raiseError(3, "dbBase")

    try:
        dbPort = root.find("dbPort").text
    except:
        log.raiseError(3, "dbPort")

    try:
        importXml_block = root.find("importXml/columns")
    except:
        log.raiseError(3, "importXml/columns")

    try:
        exportTable_block = root.find("exportTable")
    except:
        log.raiseError(3, "exportTable")
        

    importDict['testRunMode_value'] = testRunMode_value
    importDict['checkMode_value'] = checkMode_value
    importDict['importXml_path_value'] = importXml_path_value
    importDict['exportTableName_value'] = exportTableName_value
    importDict['sheetNumber_value'] = sheetNumber_value
    importDict['dbHost'] = dbHost
    importDict['dbUser'] = dbUser
    importDict['dbPass'] = dbPass
    importDict['dbBase'] = dbBase
    importDict["dbPort"] = dbPort
    importDict["loadMode"] = loadMode
    importDict["dictMode"] = dictMode

    column_block_number = 1
    for child in importXml_block.iter("column"):
        columnDict = {}

        try:
            colName = child.find("colName").text
        except:
            log.raiseError(5, "colName",column_block_number)
            
        try:
            colNameDb = child.find("colNameDb").text
        except:
            log.raiseError(5, "colNameDb", column_block_number,)
            
        try:
            colType = child.find("colType").text
        except:
            log.raiseError(5, "colType",column_block_number)
            
        try:
            isPK = child.find("isPK").text
        except:
            log.raiseError(5, "isPK",column_block_number)
            
        try:
            valueLength = child.find("valueLength").text
        except:
            log.raiseError(5, "valueLength", column_block_number)
            
        try:
            valueLength_mode = child.find("valueLength").get("mode")
        except:
            log.raiseError(6, "valueLength",column_block_number)

        try:
            transformation = child.find("transformation").text
        except:
            log.raiseError(5, "transformation",column_block_number )

        try:
            transformation_mode = child.find("transformation").get("mode")
        except:
            log.raiseError(6, "transformation", column_block_number)

        try:
            cropEnd = child.find("cropEnd").text
        except:
            log.raiseError(5, "cropEnd", column_block_number)

        try:
            cropEnd_mode = child.find("cropEnd").get("mode")
        except:
            log.raiseError(6, "cropEnd", column_block_number)

        try:
            addValueEnd = child.find("addValueEnd").text
        except:
            log.raiseError(5, "addValueEnd", column_block_number)

        try:
            addValueEnd_mode = child.find("addValueEnd").get("mode")
        except:
            log.raiseError(6, "addValueEnd", column_block_number)

        try:
            takeFromBegin = child.find("takeFromBegin").text
        except:
            log.raiseError(5, "takeFromBegin", column_block_number )

        try:
            takeFromBegin_mode = child.find("takeFromBegin").get("mode")
        except:
            log.raiseError(6, "takeFromBegin", column_block_number)

        try:
            cropBegin = child.find("cropBegin").text
        except:
            log.raiseError(5, "cropBegin",column_block_number)

        try:
            cropBegin_mode = child.find("cropBegin").get("mode")
        except:
            log.raiseError(6, "cropBegin",column_block_number)

        try:
            addValueBegin = child.find("addValueBegin").text
        except:
            log.raiseError(5, "addValueBegin",column_block_number)

        try:
            addValueBegin_mode = child.find("addValueBegin").get("mode")
        except:
            log.raiseError(6, "addValueBegin", column_block_number)

        try:
            addValueBoth = child.find("addValueBoth").text
        except:
            log.raiseError(5, "addValueBoth", column_block_number)

        try:
            addValueBoth_mode = child.find("addValueBoth").get("mode")
        except:
            log.raiseError(6, "addValueBoth",column_block_number)

        try:
            replace_mode = child.find("replace").get("mode")
        except:
            log.raiseError(5, "replace",column_block_number)
            

        replaceValArr = []
        if replace_mode == 'true':
            for repChild in child.iter("replaceVal"):
                replaceDict = {}

                try:
                    replaceValue = repChild.find("value").text
                except:
                    log.raiseError(7, "value", column_block_number)

                try:
                    replaceToValue = repChild.find("toValue").text
                except:
                    log.raiseError(7, "toValue", column_block_number)

                replaceDict["replaceValue"] = replaceValue
                replaceDict["replaceToValue"] = replaceToValue
                replaceValArr.append(replaceDict)
        else:
            replaceValArr = []

        columnDict['colName'] = colName
        columnDict['colNameDb'] = colNameDb
        columnDict['colType'] = colType
        columnDict['isPK'] = isPK
        columnDict['valueLength'] = valueLength
        columnDict['valueLength_mode'] = valueLength_mode
        columnDict['transformation'] = transformation
        columnDict['transformation_mode'] = transformation_mode
        columnDict['cropEnd'] = cropEnd
        columnDict['cropEnd_mode'] = cropEnd_mode
        columnDict['addValueEnd'] = addValueEnd
        columnDict['addValueEnd_mode'] = addValueEnd_mode
        columnDict['takeFromBegin'] = takeFromBegin
        columnDict['takeFromBegin_mode'] = takeFromBegin_mode
        columnDict['cropBegin'] = cropBegin
        columnDict['cropBegin_mode'] = cropBegin_mode
        columnDict['addValueBegin'] = addValueBegin
        columnDict['addValueBegin_mode'] = addValueBegin_mode
        columnDict['addValueBoth'] = addValueBoth
        columnDict['addValueBoth_mode'] = addValueBoth_mode
        columnDict['replace_mode'] = replace_mode
        columnDict['replaceValArr'] = replaceValArr

        colArrayExcel.append(columnDict)

        column_block_number += 1

    try:
        linkedColumns_mode = root.find("importXml/linkedColumns").get("mode")
    except:
        log.raiseError(8, "importXml/linkedColumns")

    if linkedColumns_mode == 'false' and opts.args.check_mode == 'true':
        log.raiseError(10)

    if linkedColumns_mode == 'true':
        arrOfLinkedColumns = []

        try:
            pathToLinkFile = root.find("importXml/linkedColumns/pathToLinkFile").text
        except:
            log.raiseError(3, "importXml/linkedColumns/pathToLinkFile")

        try:
            linkedFileSheetNumber = root.find("importXml/linkedColumns/linkedFileSheetNumber").text
        except:
            log.raiseError(3, "importXml/linkedColumns/linkedFileSheetNumber")

        counter = 1
        for child in root.find("importXml/linkedColumns").iter("column"):
            dictColumn = {}
            try:
                linkedColName = child.find("linkedColName").text
            except:
                log.raiseError(10, "linkedColName", counter)

            try:
                colNameInSource = child.find("colNameInSource").text
            except:
                log.raiseError(10, "colNameInSource", counter)
                
            dictColumn['linkedColName'] = linkedColName
            dictColumn['colNameInSource'] = colNameInSource
            arrOfLinkedColumns.append(dictColumn)
            counter += 1

        importDict['linkedColumns'] = arrOfLinkedColumns
        importDict['pathToLinkFile'] = pathToLinkFile
        importDict['linkedFileSheetNumber'] = int(linkedFileSheetNumber) - 1

    try:
        withDict_mode = root.find("importXml/withDict").get("mode")
    except:
        log.raiseError(8, "importXml/withDict")

    importDict["withDict_mode"] = withDict_mode

    if root.find("dict").text == 'true' and withDict_mode == 'false':
        log.raiseError('Error - <--dict true> but if you want to load with dict you must to set <withDict mode="true">')
        


    if root.find("dict").text == 'true':
        dict = []

        try:
            dictTableName = root.find("importXml/withDict/dictTableName").text
        except:
            log.raiseError(3, "importXml/withDict/dictTableName")

        importDict['dictTableName'] = dictTableName

        counter = 1
        for child in root.find("importXml/withDict").iter("column"):
            arrOfDictColumns = {}
            try:
                colName = child.find("colName").text
            except:
                log.raiseError(11, "colName", column_block_number)

            try:
                colNameDb = child.find("colNameDb").text
            except:
                log.raiseError(11, "colNameDb", column_block_number, )

            try:
                colType = child.find("colType").text
            except:
                log.raiseError(11, "colType", column_block_number)

            try:
                isPK = child.find("isPK").text
            except:
                log.raiseError(11, "isPK", column_block_number)

            try:
                valueLength = child.find("valueLength").text
            except:
                log.raiseError(11, "valueLength", column_block_number)

            try:
                valueLength_mode = child.find("valueLength").get("mode")
            except:
                log.raiseError(12, "valueLength", column_block_number)

            try:
                transformation = child.find("transformation").text
            except:
                log.raiseError(11, "transformation", column_block_number)

            try:
                transformation_mode = child.find("transformation").get("mode")
            except:
                log.raiseError(12, "transformation", column_block_number)

            try:
                cropEnd = child.find("cropEnd").text
            except:
                log.raiseError(11, "cropEnd", column_block_number)

            try:
                cropEnd_mode = child.find("cropEnd").get("mode")
            except:
                log.raiseError(12, "cropEnd", column_block_number)

            try:
                addValueEnd = child.find("addValueEnd").text
            except:
                log.raiseError(11, "addValueEnd", column_block_number)

            try:
                addValueEnd_mode = child.find("addValueEnd").get("mode")
            except:
                log.raiseError(12, "addValueEnd", column_block_number)

            try:
                takeFromBegin = child.find("takeFromBegin").text
            except:
                log.raiseError(11, "takeFromBegin", column_block_number)

            try:
                takeFromBegin_mode = child.find("takeFromBegin").get("mode")
            except:
                log.raiseError(12, "takeFromBegin", column_block_number)

            try:
                cropBegin = child.find("cropBegin").text
            except:
                log.raiseError(11, "cropBegin", column_block_number)

            try:
                cropBegin_mode = child.find("cropBegin").get("mode")
            except:
                log.raiseError(12, "cropBegin", column_block_number)

            try:
                addValueBegin = child.find("addValueBegin").text
            except:
                log.raiseError(11, "addValueBegin", column_block_number)

            try:
                addValueBegin_mode = child.find("addValueBegin").get("mode")
            except:
                log.raiseError(12, "addValueBegin", column_block_number)

            try:
                addValueBoth = child.find("addValueBoth").text
            except:
                log.raiseError(11, "addValueBoth", column_block_number)

            try:
                addValueBoth_mode = child.find("addValueBoth").get("mode")
            except:
                log.raiseError(12, "addValueBoth", column_block_number)

            try:
                replace_mode = child.find("replace").get("mode")
            except:
                log.raiseError(11, "replace", column_block_number)

            replaceValArr = []
            if replace_mode == 'true':
                for repChild in child.iter("replaceVal"):
                    replaceDict = {}

                    try:
                        replaceValue = repChild.find("value").text
                    except:
                        log.raiseError(13, "value", column_block_number)

                    try:
                        replaceToValue = repChild.find("toValue").text
                    except:
                        log.raiseError(13, "toValue", column_block_number)

                    replaceDict["replaceValue"] = replaceValue
                    replaceDict["replaceToValue"] = replaceToValue
                    replaceValArr.append(replaceDict)
            else:
                replaceValArr = []

            arrOfDictColumns['colName'] = colName
            arrOfDictColumns['colNameDb'] = colNameDb
            arrOfDictColumns['colType'] = colType
            arrOfDictColumns['isPK'] = isPK
            arrOfDictColumns['valueLength'] = valueLength
            arrOfDictColumns['valueLength_mode'] = valueLength_mode
            arrOfDictColumns['transformation'] = transformation
            arrOfDictColumns['transformation_mode'] = transformation_mode
            arrOfDictColumns['cropEnd'] = cropEnd
            arrOfDictColumns['cropEnd_mode'] = cropEnd_mode
            arrOfDictColumns['addValueEnd'] = addValueEnd
            arrOfDictColumns['addValueEnd_mode'] = addValueEnd_mode
            arrOfDictColumns['takeFromBegin'] = takeFromBegin
            arrOfDictColumns['takeFromBegin_mode'] = takeFromBegin_mode
            arrOfDictColumns['cropBegin'] = cropBegin
            arrOfDictColumns['cropBegin_mode'] = cropBegin_mode
            arrOfDictColumns['addValueBegin'] = addValueBegin
            arrOfDictColumns['addValueBegin_mode'] = addValueBegin_mode
            arrOfDictColumns['addValueBoth'] = addValueBoth
            arrOfDictColumns['addValueBoth_mode'] = addValueBoth_mode
            arrOfDictColumns['replace_mode'] = replace_mode
            arrOfDictColumns['replaceValArr'] = replaceValArr

            dict.append(arrOfDictColumns)

            counter += 1
    # ---------------
        importDict['withDict'] = dict
    importDict["excelColumns"] = colArrayExcel

    column_block_number = 1
    for child in exportTable_block.iter("column"):
        columnDict = {}

        try:
            colName = child.find("name").text
        except:
            log.raiseError(14, "name", column_block_number)
            
        try:
            isAutoInc = child.find("isAutoInc").text
        except:
            log.raiseError(14, "isAutoInc", column_block_number)

        try:
            isConc = child.find("isConc").text
        except:
            log.raiseError(14, "isConc", column_block_number)

        try:
            fromExcel = child.find("fromExcel").text
        except:
            log.raiseError(14, "fromExcel", column_block_number)

        try:
            defaultValue = child.find("defaultValue").text
        except:
            log.raiseError(14, "defaultValue", column_block_number)

        try:
            defaultValue_mode = child.find("defaultValue").get("mode")
        except:
            log.raiseError(15, "defaultValue", column_block_number)

        try:
            colType = child.find("colType").text
        except:
            log.raiseError(14, "colType", column_block_number)
            
        try:
            ifNull = child.find("ifNull").text
        except:
            log.raiseError(14, "ifNull", column_block_number)

        try:
            ifNull_mode = child.find("ifNull").get("mode")
        except:
            log.raiseError(15, "ifNull", column_block_number)

        try:
            isUpdateCondition = child.find("isUpdateCondition").text
        except:
            log.raiseError(14, "isUpdateCondition", column_block_number)

        try:
            fromDb = child.find("fromDb").text
        except:
            log.raiseError(14, "fromDb", column_block_number)
            

        columnDict["colName"] = colName
        columnDict["fromExcel"] = fromExcel
        columnDict["defaultValue"] = defaultValue
        columnDict["defaultValue_mode"] = defaultValue_mode
        columnDict["colType"] = colType
        columnDict["ifNull"] = ifNull
        columnDict["ifNull_mode"] = ifNull_mode
        columnDict["isAutoInc"] = isAutoInc
        columnDict["isConc"] = isConc
        columnDict["isUpdateCondition"] = isUpdateCondition
        columnDict["fromDb"] = fromDb

        colArrayDB.append(columnDict)

        column_block_number += 1

    importDict["dbColumns"] = colArrayDB

    return importDict



