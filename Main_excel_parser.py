import Query_creator as qc
import XML_DB_DAO as xpc
import Logger
import Validate_res
from Opt_parser import Opts

opts = Opts()

for pathToConfigXML in opts.args.config:
    loggerInst = Logger.Log_info.getInstance(pathToConfigXML)
    loggerInst.raiseInfo(4)
    dbService = xpc.XmlParser(pathToConfigXML, loggerInst, opts)
    dbService.connectToTheDB(loggerInst)
    validator = Validate_res.Validate(dbService, loggerInst, opts)
    validator.validate()

    if opts.args.check_mode == 'true':
        dbService.closeConnect(loggerInst)
        loggerInst.raiseInfo(7)
        break

    queryService = qc.Query(dbService, loggerInst, opts)
    queryService.execAllQueries()

    loggerInst.raiseInfo(7)

dbService.closeConnect(loggerInst)

