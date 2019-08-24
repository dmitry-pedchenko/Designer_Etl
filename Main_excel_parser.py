import sys
import os
sys.path.append(os.path.join(os.getcwd(), "venv", "Lib", "site-packages"))

import Query_creator as qc
import XML_DAO as xpc
import Logger
import Validate_res
from Opt_parser import Opts
from DB_connector import Connection as con

opts = Opts()

connector = None

for pathToConfigXML in opts.args.config:
    loggerInst = Logger.Log_info.getInstance(pathToConfigXML, opts.args.config)
    loggerInst.set_config(pathToConfigXML)
    loggerInst.raiseInfo(4)
    dbService = xpc.XmlParser(pathToConfigXML, loggerInst, opts)

    connector = con.get_instance(loggerInst)
    connector.connectToTheDB(
                             dbService.dictionary["dbHost"],
                             dbService.dictionary["dbUser"],
                             dbService.dictionary["dbPass"],
                             dbService.dictionary["dbBase"],
                             dbService.dictionary["dbPort"],
                             dbService.dictionary["dbtype"])

    validator = Validate_res.Validate(dbService, loggerInst, opts, connector)
    validator.validate()

    if dbService.dictionary['checkMode_value'] == 'true':
        connector.closeConnect()
        loggerInst.raiseInfo(7)
        break

    queryService = qc.Query(dbService, loggerInst, opts, connector)
    queryService.execAllQueries()

    loggerInst.raiseInfo(7)

if connector:
    connector.closeConnect()


