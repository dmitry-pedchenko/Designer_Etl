import sys
import os
sys.path.append(os.path.join(os.getcwd(), "env", "Lib", "site-packages"))

from Logger import Logger
from Validate import Validate_res
from Query import Query_creator as qc
from DAO import XML_DAO as xpc
from Parser.Opt_parser import Opts
from DAO.DB_connector import Connection as con

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


