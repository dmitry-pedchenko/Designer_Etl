import xml.etree.ElementTree as et
import os


def do_XML_parse(pathToFile, log, opts=None):
    colArrayExcel = []  # массив включающий в себя все колонки из источника
    importDict = {}  # словарь для каждой колонки
    colArrayDB = []  # массив с колонками в базе

    pathToFile = os.path.join(os.path.join(os.getcwd(), 'config'), pathToFile)

    try:
        root = et.parse(pathToFile).getroot()
    except Exception as e:
        log.raiseError(1, e)

    try:
        sheetNumber_value = int(root.find("importXml/sheetNumber").text) - 1
    except:
        log.raiseError(3, "importXml/sheetNumber")

    if opts:
        try:
            testRunMode_value = opts.args.test_mode
        except:
            log.raiseError(4, "test_mode")
    else:
        testRunMode_value='true'

    try:
        dbtype= root.find("dbtype").text
    except:
        log.raiseError(3, "dbtype")

    try:
        dictMode= root.find("dict").text
    except:
        log.raiseError(3, "dict")

    try:
        loadMode= root.find("loadMode").text
    except:
        log.raiseError(3, "loadMode")

    try:
        checkMode_value = root.find("checkMode").text
    except:
        log.raiseError(4, "checkMode")

    try:
        db_schema = root.find("dbSchema").text
    except:
        log.raiseError(4, "dbSchema")

    try:
        importXml_path_value = root.find("importXml/path").text
    except:
        log.raiseError(3, "importXml/path")

    try:
        exportTableName_value_text = root.find("exportTable/path").text
    except:
        log.raiseError(3, "exportTable/path")

    if dbtype == 'mssql':
        exportTableName_value = f"[{db_schema}].[{exportTableName_value_text}]"
    elif dbtype == 'mysql':
        exportTableName_value = f"{db_schema}.{exportTableName_value_text}"

    # if checkMode_value == 'false':
        # try:
        #     exportTableName_value_text = root.find("exportTable/path").text
        # except:
        #     log.raiseError(3, "exportTable/path")

        # if dbtype == 'mssql':
        #     exportTableName_value = f"[{db_schema}].[{exportTableName_value_text}]"
        # elif dbtype == 'mysql':
        #     exportTableName_value = f"{db_schema}.{exportTableName_value_text}"

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

    importDict['db_schema'] = db_schema
    importDict['testRunMode_value'] = testRunMode_value
    importDict['checkMode_value'] = checkMode_value
    importDict['importXml_path_value'] = importXml_path_value

    importDict['exportTableName_value_text'] = exportTableName_value_text
    importDict['exportTableName_value'] = exportTableName_value

    # if checkMode_value == 'false':
    #     importDict['exportTableName_value_text'] = exportTableName_value_text
    #     importDict['exportTableName_value'] = exportTableName_value
    importDict['sheetNumber_value'] = sheetNumber_value
    importDict['dbHost'] = dbHost
    importDict['dbUser'] = dbUser
    importDict['dbPass'] = dbPass
    importDict['dbBase'] = dbBase
    importDict["dbPort"] = dbPort
    importDict["loadMode"] = loadMode
    importDict["dictMode"] = dictMode
    importDict["dbtype"] = dbtype

    for column_block_number, child in enumerate(importXml_block.iter("column")):
        columnDict = {}

        try:
            colName = child.find("colName").text
        except:
            log.raiseError(5, "colName",column_block_number)

        try:
            colNameDb = child.find("colNameDb").text
        except:
            log.raiseError(5, "colNameDb", column_block_number, )

        # if checkMode_value == 'false':
        #     try:
        #         colNameDb = child.find("colNameDb").text
        #     except:
        #         log.raiseError(5, "colNameDb", column_block_number,)
            
        try:
            colType = child.find("colType").text
        except:
            log.raiseError(5, "colType",column_block_number)
            
        try:
            isPK = child.find("isPK").text
        except:
            log.raiseError(5, "isPK",column_block_number)

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
            log.raiseError(5, "replace", column_block_number)
            

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

        try:
            filter_mode = child.find("filter").get("mode")
        except:
            log.raiseError(5, "filter", column_block_number)

        filterArr = []

        if filter_mode == 'true':
            filter_dict_edit = {}

            try:
                f_cropEnd = child.find("filter/f_cropEnd").text
            except:
                f_log.raiseError(5, "filter/f_cropEnd", column_block_number)

            try:
                f_cropEnd_mode = child.find("filter/f_cropEnd").get("mode")
            except:
                log.raiseError(6, "filter/f_cropEnd", column_block_number)

            try:
                f_addValueEnd = child.find("filter/f_addValueEnd").text
            except:
                log.raiseError(5, "filter/f_addValueEnd", column_block_number)

            try:
                f_addValueEnd_mode = child.find("filter/f_addValueEnd").get("mode")
            except:
                log.raiseError(6, "filter/f_addValueEnd", column_block_number)

            try:
                f_takeFromBegin = child.find("filter/f_takeFromBegin").text
            except:
                log.raiseError(5, "filter/f_takeFromBegin", column_block_number)

            try:
                f_takeFromBegin_mode = child.find("filter/f_takeFromBegin").get("mode")
            except:
                log.raiseError(6, "filter/f_takeFromBegin", column_block_number)

            try:
                f_cropBegin = child.find("filter/f_cropBegin").text
            except:
                log.raiseError(5, "filter/f_cropBegin", column_block_number)

            try:
                f_cropBegin_mode = child.find("filter/f_cropBegin").get("mode")
            except:
                log.raiseError(6, "filter/f_cropBegin", column_block_number)

            try:
                f_addValueBegin = child.find("filter/f_addValueBegin").text
            except:
                log.raiseError(5, "filter/f_addValueBegin", column_block_number)

            try:
                f_addValueBegin_mode = child.find("filter/f_addValueBegin").get("mode")
            except:
                log.raiseError(6, "filter/f_addValueBegin", column_block_number)

            try:
                f_addValueBoth = child.find("filter/f_addValueBoth").text
            except:
                log.raiseError(5, "filter/f_addValueBoth", column_block_number)

            try:
                f_addValueBoth_mode = child.find("filter/f_addValueBoth").get("mode")
            except:
                log.raiseError(6, "filter/f_addValueBoth", column_block_number)

            filter_dict_edit["cropEnd"] = f_cropEnd
            filter_dict_edit["cropEnd_mode"] = f_cropEnd_mode
            filter_dict_edit["addValueEnd"] = f_addValueEnd
            filter_dict_edit["addValueEnd_mode"] = f_addValueEnd_mode
            filter_dict_edit["takeFromBegin"] = f_takeFromBegin
            filter_dict_edit["takeFromBegin_mode"] = f_takeFromBegin_mode
            filter_dict_edit["cropBegin"] = f_cropBegin
            filter_dict_edit["cropBegin_mode"] = f_cropBegin_mode
            filter_dict_edit["addValueBegin"] = f_addValueBegin
            filter_dict_edit["addValueBegin_mode"] = f_addValueBegin_mode
            filter_dict_edit["addValueBoth"] = f_addValueBoth
            filter_dict_edit["addValueBoth_mode"] = f_addValueBoth_mode



            for child_filter in child.iter("filterVal"):
                filterDict = {}

                try:
                    filterMode = child_filter.find("filterMode").text
                except:
                    log.raiseError(7, "filterMode", column_block_number)

                try:
                    filterValue = child_filter.find("filterValue").text
                except:
                    log.raiseError(7, "filterValue", column_block_number)

                filterDict["filterMode"] = filterMode
                filterDict["filterValue"] = filterValue
                filterArr.append(filterDict)

        try:
            post_filter_mode = child.find("post-filter").get("mode")
        except:
            log.raiseError(5, "post-filter", column_block_number)

        postfilterArr = []

        if post_filter_mode == 'true':
            for child_filter in child.iter("postfilterVal"):
                filterDict = {}

                try:
                    filterMode = child_filter.find("filterMode").text
                except:
                    log.raiseError(7, "filterMode", column_block_number)

                try:
                    filterValue = child_filter.find("filterValue").text
                except:
                    log.raiseError(7, "filterValue", column_block_number)

                filterDict["filterMode"] = filterMode
                filterDict["filterValue"] = filterValue
                postfilterArr.append(filterDict)

        if cropEnd_mode == 'true':
            try:
                int(cropEnd)
            except:
                log.raiseError(40, 'importXml/columns', cropEnd, column_block_number)
        if takeFromBegin_mode == 'true':
            try:
                int(takeFromBegin)
            except:
                log.raiseError(40,  'importXml/columns', takeFromBegin, column_block_number)
        if cropBegin_mode == 'true':
            try:
                int(cropBegin)
            except:
                log.raiseError(40, 'importXml/columns', cropBegin, column_block_number)

        columnDict['colName'] = colName

        columnDict['colNameDb'] = colNameDb

        # if checkMode_value == 'false':
        #     columnDict['colNameDb'] = colNameDb
        columnDict['colType'] = colType
        columnDict['isPK'] = isPK
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
        columnDict['filter_mode'] = filter_mode
        columnDict['filterArr'] = filterArr
        columnDict['post_filter_mode'] = post_filter_mode
        columnDict['postfilterArr'] = postfilterArr
        if filter_mode == 'true':
            columnDict['filter_dict_edit'] = filter_dict_edit


        colArrayExcel.append(columnDict)
    importDict["excelColumns"] = colArrayExcel

    try:
        linkedColumns_mode = root.find("importXml/linkedColumns").get("mode")
    except:
        log.raiseError(8, "importXml/linkedColumns")

    if linkedColumns_mode == 'false' and checkMode_value == 'true':
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

        try:
            if_both = root.find("importXml/linkedColumns/both").text
        except:
            log.raiseError(3, "importXml/linkedColumns/both")

        for counter, child in enumerate(root.find("importXml/linkedColumns").iter("column"), 1):
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


        importDict['linkedColumns'] = arrOfLinkedColumns
        importDict['if_both'] = if_both
        importDict['pathToLinkFile'] = pathToLinkFile
        importDict['linkedFileSheetNumber'] = int(linkedFileSheetNumber) - 1

    # if checkMode_value == 'false':
    try:
        withDict_mode = root.find("importXml/withDict").get("mode")
    except:
        log.raiseError(8, "importXml/withDict")

    try:
        root.find("importXml/withDict").text
    except:
        log.raiseError(3, "importXml/withDict")

    importDict["withDict_mode"] = withDict_mode

    if root.find("dict").text == 'true' and withDict_mode == 'false':
        log.raiseError('Error - <dict>true</dict> but if you want to load with dict you must to set <withDict mode="true">')

    if root.find("dict").text == 'true':
        dict = []

        try:
            dictTableName = root.find("importXml/withDict/tables")
        except:
            log.raiseError(3, "importXml/withDict/tables")

        for col_tables_number, table in enumerate(dictTableName.iter('table'), 1):
            table_arr = {}
            arr_of_columns = []

            try:
                table_arr['dictTableName'] = table.find('dictTableName').text
            except:
                log.raiseError(11, 'dictTableName', col_tables_number)

            try:
                table_arr['indxDbColumn'] = table.find('indxDbColumn').text
            except:
                log.raiseError(11, 'indxDbColumn', col_tables_number)

            try:
                table_arr['indxColumnDic'] = table.find('indxColumnDic').text
            except:
                log.raiseError(11, 'indxColumnDic', col_tables_number)


            for column_block_number, child in enumerate(table.iter("column"), 1):
                arrOfDictColumns = {}
                try:
                    colName = child.find("colName").text
                except:
                    log.raiseError(11, "colName", column_block_number)

                try:
                    colNameDb = child.find("colNameDb").text
                except:
                    log.raiseError(11, "colNameDb", column_block_number)

                try:
                    colType = child.find("colType").text
                except:
                    log.raiseError(11, "colType", column_block_number)

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


                if cropEnd_mode == 'true':
                    try:
                        int(cropEnd)
                    except:
                        log.raiseError(40, 'withDict/columns', cropEnd, column_block_number)
                if takeFromBegin_mode == 'true':
                    try:
                        int(takeFromBegin)
                    except:
                        log.raiseError(40, 'withDict/columns', takeFromBegin, column_block_number)
                if cropBegin_mode == 'true':
                    try:
                        int(cropBegin)
                    except:
                        log.raiseError(40, 'withDict/columns', cropBegin, column_block_number)

                arrOfDictColumns['colName'] = colName
                arrOfDictColumns['colNameDb'] = colNameDb
                arrOfDictColumns['colType'] = colType
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


                arr_of_columns.append(arrOfDictColumns)
            table_arr['arrOfDictColumns'] = arr_of_columns
            dict.append(table_arr)

        importDict['withDict'] = dict
# ---

    for column_block_number, child in enumerate(exportTable_block.iter("column"), 1):
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


    importDict["dbColumns"] = colArrayDB

    return importDict



