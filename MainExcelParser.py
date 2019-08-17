import queryCreator as qc
import XmlParserClass as xpc
import logger
import validateRes
from OptParser import Opts

opts = Opts()

for pathToConfigXML in opts.args.config:
    loggerInst = logger.logInfo.getInstance(pathToConfigXML)

    loggerInst.logger.info("Starts executing... {}".format(pathToConfigXML))

    dbService = xpc.XmlParser(pathToConfigXML, loggerInst, opts)
    dbService.connectToTheDB(loggerInst)
    validator = validateRes.Validate(dbService, loggerInst, opts)
    validator.validate()

    if opts.args.check_mode == 'true':
        dbService.closeConnect(loggerInst)
        loggerInst.logger.info("Ends executing... Success <{}>\n".format(pathToConfigXML))
        break

    queryService = qc.Query(dbService, loggerInst, opts)
    queryService.execAllQueries()

    dbService.closeConnect(loggerInst)
    loggerInst.logger.info("Ends executing... Success <{}>\n".format(pathToConfigXML))
