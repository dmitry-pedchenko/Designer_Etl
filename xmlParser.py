import xml.etree.ElementTree as et
import os


def xmlParse(pathToFile, log, opts):
    colArrayExcel = []  # массив включающий в себя все колонки из источника
    importDict = {}  # словарь для каждой колонки
    colArrayDB = []  # массив с колонками в базе

    pathToFile = os.path.join(os.path.join(os.getcwd(), 'config'), pathToFile)

    try:    root = et.parse(pathToFile).getroot()
    except Exception as e:
        log.logger.error("Error 2 - Cant find file XML " + pathToFile + "\n" + e.args[0])
        raise SystemExit(1)

    try:    sheetNumber_value = int(root.find("importXml/sheetNumber").text) - 1
    except:
        log.logger.error("Error 3 - Can't find tag <importXml/sheetNumber> in xml")
        raise SystemExit(1)

    try:     testRunMode_value = opts.args.test_mode
    except:
        log.logger.error("Error - Can't find --test_mode")
        raise SystemExit(1)

    try:     dictMode= root.find("dict").text
    except:
        log.logger.error("Error - Can't find <dict>")
        raise SystemExit(1)

    try:     loadMode= root.find("loadMode").text
    except:
        log.logger.error("Error - Can't find <loadMode>")
        raise SystemExit(1)


    try:     checkMode_value = opts.args.check_mode
    except:
        log.logger.error("Error - Can't find --check_mode")
        raise SystemExit(1)


    try:    importXml_path_value = root.find("importXml/path").text
    except:
        log.logger.error("Error 3 - Can't find tag <importXml/path> in xml")
        raise SystemExit(1)


    try:     exportTableName_value = root.find("exportTable/path").text
    except:
        log.logger.error("Error 3 - Can't find tag <exportTable/path> in xml")
        raise SystemExit(1)


    try:    dbHost = root.find("dbHost").text
    except:
        log.logger.error("Error 3 - Can't find tag <dbHost> in xml")
        raise SystemExit(1)


    try:     dbUser = root.find("dbUser").text
    except:
        log.logger.error("Error 3 - Can't find tag <dbUser> in xml")
        raise SystemExit(1)


    try:        dbPass = root.find("dbPass").text
    except:
        log.logger.error("Error 3 - Can't find tag <dbPass> in xml")
        raise SystemExit(1)


    try:        dbBase = root.find("dbBase").text
    except:
        log.logger.error("Error 3 - Can't find tag <dbBase> in xml")
        raise SystemExit(1)


    try:        dbPort = root.find("dbPort").text
    except:
        log.logger.error("Error 3 - Can't find tag <dbPort> in xml")
        raise SystemExit(1)


    try:        importXml_block = root.find("importXml/columns")
    except:
        log.logger.error("Error 3 - Can't find tag <importXml/columns> in xml")
        raise SystemExit(1)


    try:     exportTable_block = root.find("exportTable")
    except:
        log.logger.error("Error 3 - Can't find tag <exportTable> in xml")
        raise SystemExit(1)

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

        try:         colName = child.find("colName").text
        except:
            log.logger.error("Error 4 - Can't find tag <colName> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)
        try:            colNameDb = child.find("colNameDb").text
        except:
            log.logger.error("Error 4 - Can't find tag <colNameDb> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)
        try:            colType = child.find("colType").text
        except:
            log.logger.error("Error 4 - Can't find tag <colType> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)
        try:            isPK = child.find("isPK").text
        except:
            log.logger.error("Error 4 - Can't find tag <isPK> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)
        try:            valueLength = child.find("valueLength").text
        except:
            log.logger.error("Error 4 - Can't find tag <valueLength> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)
        try:            valueLength_mode = child.find("valueLength").get("mode")
        except:
            log.logger.error("Error 5 - Can't find property mode in tag <valueLength> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            transformation = child.find("transformation").text
        except:
            log.logger.error("Error 4 - Can't find tag <transformation> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            transformation_mode = child.find("transformation").get("mode")
        except:
            log.logger.error("Error 5 - Can't find property mode in tag <transformation> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            cropEnd = child.find("cropEnd").text
        except:
            log.logger.error("Error 4 - Can't find tag <cropEnd> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            cropEnd_mode = child.find("cropEnd").get("mode")
        except:
            log.logger.error("Error 4 - Can't find property mode in tag <cropEnd> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)


        try:            addValueEnd = child.find("addValueEnd").text
        except:
            log.logger.error("Error 4 - Can't find tag <addValueEnd> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            addValueEnd_mode = child.find("addValueEnd").get("mode")
        except:
            log.logger.error("Error 5 - Can't find property mode in tag <addValueEnd> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            takeFromBegin = child.find("takeFromBegin").text
        except:
            log.logger.error("Error 4 - Can't find tag <takeFromBegin> in <column> tag at block number <{}> in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            takeFromBegin_mode = child.find("takeFromBegin").get("mode")
        except:
            log.logger.error("Error 5 - Can't find property mode in tag <takeFromBegin> in <column> tag at block number {} in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            cropBegin = child.find("cropBegin").text
        except:
            log.logger.error("Error 4 - Can't find tag <cropBegin> in <column> tag at block number {} in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            cropBegin_mode = child.find("cropBegin").get("mode")
        except:
            log.logger.error("Error 5 - Can't find property mode in tag <cropBegin> in <column> tag at block number {} in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:    addValueBegin = child.find("addValueBegin").text
        except:
            log.logger.error("Error 4 - Can't find tag <addValueBegin> in <column> tag at block number {} in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            addValueBegin_mode = child.find("addValueBegin").get("mode")
        except:
            log.logger.error("Error 5 - Can't find property mode in tag <addValueBegin> in <column> tag at block number {} in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            addValueBoth = child.find("addValueBoth").text
        except:
            log.logger.error("Error 4 - Can't find tag <addValueBoth> in <column> tag at block number {} in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            addValueBoth_mode = child.find("addValueBoth").get("mode")
        except:
            log.logger.error("Error 5 - Can't find property mode in tag <addValueBoth> in <column> tag at block number {} in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            replace_mode = child.find("replace").get("mode")
        except:
            log.logger.error("Error 4 - Can't find tag <replace> in <column> tag at block number {} in importXml/columns block in xml".format(column_block_number))
            raise SystemExit(1)

        replaceValArr = []
        if replace_mode == 'true':
            for repChild in child.iter("replaceVal"):
                replaceDict = {}

                try:                    replaceValue = repChild.find("value").text
                except:
                    log.logger.error("Error 4 - Can't find tag <value> in <replace> tag at block number {} in importXml/columns block in xml".format(column_block_number))
                    raise SystemExit(1)

                try:                    replaceToValue = repChild.find("toValue").text
                except:
                    log.logger.error("Error 4 - Can't find tag <toValue> in <replace> tag at block number {} in importXml/columns block in xml".format(column_block_number))
                    raise SystemExit(1)


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
        log.logger.error(
            "Error 3 - Can't find property mode in tag <importXml/linkedColumns>  in xml")
        raise SystemExit(1)


    if linkedColumns_mode == 'false' and opts.args.check_mode == 'true':
        log.logger.error('If you want to check source file you must to set <linkedColumns mode="true">')
        raise SystemExit(1)


    if linkedColumns_mode == 'true':
        arrOfLinkedColumns = []

        try:    pathToLinkFile = root.find("importXml/linkedColumns/pathToLinkFile").text
        except:
            log.logger.error(
                "Error 3 - Can't find tag <importXml/linkedColumns/pathToLinkFile>  in xml")
            raise SystemExit(1)

        try:    linkedFileSheetNumber = root.find("importXml/linkedColumns/linkedFileSheetNumber").text
        except:
            log.logger.error(
                "Error 3 - Can't find tag <importXml/linkedColumns/linkedFileSheetNumber>  in xml")
            raise SystemExit(1)

        counter = 1

        for child in root.find("importXml/linkedColumns").iter("column"):
            dictColumn = {}
            try: linkedColName = child.find("linkedColName").text
            except:
                log.logger.error(
                    "Error  - Can't find tag <linkedColName> at block number {} in <importXml/linkedColumns>  in xml".format(counter))
                raise SystemExit(1)

            try: colNameInSource = child.find("colNameInSource").text
            except:
                log.logger.error(
                    "Error  - Can't find tag <colNameInSource>  at block number {} in <importXml/linkedColumns>  in xml".format(counter))
                raise SystemExit(1)
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
        log.logger.error(
            "Error 3 - Can't find property mode in tag <importXml/withDict>  in xml")
        raise SystemExit(1)

    importDict["withDict_mode"] = withDict_mode

    if root.find("dict").text == 'true' and withDict_mode == 'false':
        log.logger.error('Error - <--dict true> but if you want to load with dict you must to set <withDict mode="true">')
        raise SystemExit(1)


    if root.find("dict").text == 'true':
        dict = []

        try:    dictTableName = root.find("importXml/withDict/dictTableName").text
        except:
            log.logger.error(
                "Error 3 - Can't find tag <importXml/withDict/dictTableName>  in xml")
            raise SystemExit(1)

        importDict['dictTableName'] = dictTableName


        counter = 1
        for child in root.find("importXml/withDict").iter("column"):
            arrOfDictColumns = {}
            try:
                colName = child.find("colName").text
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <colName> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)
            try:
                colNameDb = child.find("colNameDb").text
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <colNameDb> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)
            try:
                colType = child.find("colType").text
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <colType> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)
            try:
                isPK = child.find("isPK").text
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <isPK> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)
            try:
                valueLength = child.find("valueLength").text
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <valueLength> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)
            try:
                valueLength_mode = child.find("valueLength").get("mode")
            except:
                log.logger.error(
                    "Error 5 - Can't find property mode in tag <valueLength> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                transformation = child.find("transformation").text
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <transformation> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                transformation_mode = child.find("transformation").get("mode")
            except:
                log.logger.error(
                    "Error 5 - Can't find property mode in tag <transformation> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                cropEnd = child.find("cropEnd").text
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <cropEnd> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                cropEnd_mode = child.find("cropEnd").get("mode")
            except:
                log.logger.error(
                    "Error 4 - Can't find property mode in tag <cropEnd> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                addValueEnd = child.find("addValueEnd").text
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <addValueEnd> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                addValueEnd_mode = child.find("addValueEnd").get("mode")
            except:
                log.logger.error(
                    "Error 5 - Can't find property mode in tag <addValueEnd> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                takeFromBegin = child.find("takeFromBegin").text
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <takeFromBegin> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                takeFromBegin_mode = child.find("takeFromBegin").get("mode")
            except:
                log.logger.error(
                    "Error 5 - Can't find property mode in tag <takeFromBegin> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                cropBegin = child.find("cropBegin").text
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <cropBegin> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                cropBegin_mode = child.find("cropBegin").get("mode")
            except:
                log.logger.error(
                    "Error 5 - Can't find property mode in tag <cropBegin> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                addValueBegin = child.find("addValueBegin").text
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <addValueBegin> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                addValueBegin_mode = child.find("addValueBegin").get("mode")
            except:
                log.logger.error(
                    "Error 5 - Can't find property mode in tag <addValueBegin> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                addValueBoth = child.find("addValueBoth").text
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <addValueBoth> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                addValueBoth_mode = child.find("addValueBoth").get("mode")
            except:
                log.logger.error(
                    "Error 5 - Can't find property mode in tag <addValueBoth> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            try:
                replace_mode = child.find("replace").get("mode")
            except:
                log.logger.error(
                    "Error 4 - Can't find tag <replace> in <column> tag at block number {} in importXml/withDict block in xml".format(
                        column_block_number))
                raise SystemExit(1)

            replaceValArr = []
            if replace_mode == 'true':
                for repChild in child.iter("replaceVal"):
                    replaceDict = {}

                    try:
                        replaceValue = repChild.find("value").text
                    except:
                        log.logger.error(
                            "Error 4 - Can't find tag <value> in <replace> tag at block number {} in importXml/withDict block in xml".format(
                                column_block_number))
                        raise SystemExit(1)

                    try:
                        replaceToValue = repChild.find("toValue").text
                    except:
                        log.logger.error(
                            "Error 4 - Can't find tag <toValue> in <replace> tag at block number {} in importXml/withDict block in xml".format(
                                column_block_number))
                        raise SystemExit(1)

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

        try:            colName = child.find("name").text
        except:
            log.logger.error("Error 6 - Can't find tag <name> in <column> tag at block number {} in exportTable block in xml".format(column_block_number))
            raise SystemExit(1)
        try:            isAutoInc = child.find("isAutoInc").text
        except:
            log.logger.error("Error 6 - Can't find tag <isAutoInc> in <column> tag at block number {} in exportTable block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            isConc = child.find("isConc").text
        except:
            log.logger.error("Error 6 - Can't find tag <isConc> in <column> tag at block number {} in exportTable block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            fromExcel = child.find("fromExcel").text
        except:
            log.logger.error("Error 6 - Can't find tag <fromExcel> in <column> tag at block number {} in exportTable block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            defaultValue = child.find("defaultValue").text
        except:
            log.logger.error("Error 6 - Can't find tag <defaultValue> in <column> tag at block number {} in exportTable block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            defaultValue_mode = child.find("defaultValue").get("mode")
        except:
            log.logger.error("Error 7 - Can't find property mode in tag <defaultValue> in <column> tag at block number {} in exportTable block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            colType = child.find("colType").text
        except:
            log.logger.error("Error 6 - Can't find tag <colType> in <column> tag at block number {} in exportTable block in xml".format(column_block_number))
            raise SystemExit(1)
        try:            ifNull = child.find("ifNull").text
        except:
            log.logger.error("Error 6 - Can't find tag <ifNull> in <column> tag at block number {} in exportTable block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            ifNull_mode = child.find("ifNull").get("mode")
        except:
            log.logger.error("Error 7 - Can't find property mode in tag <ifNull> in <column> tag at block number {} in exportTable block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            isUpdateCondition = child.find("isUpdateCondition").text
        except:
            log.logger.error("Error 7 - Can't find tag <isUpdateCondition> in <column> tag at block number {} in exportTable block in xml".format(column_block_number))
            raise SystemExit(1)

        try:            fromDb = child.find("fromDb").text
        except:
            log.logger.error("Error 7 - Can't find tag <fromDb> in <column> tag at block number {} in exportTable block in xml".format(column_block_number))
            raise SystemExit(1)

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



