import datetime
import logging
import os


class logInfo:
    __instance = None

    @classmethod
    def getInstance(cls, pathToConfigXML):
        if not cls.__instance:
            cls.__instance = logInfo(pathToConfigXML)
        return cls.__instance

    def __init__(self, pathToConfigXML):
        self.getLogger(pathToConfigXML)

    def getLogger(self, pathToConfigXML):
        currentPath = os.getcwd()
        pathToLogFolder = os.path.join(currentPath, 'log')  # folder log
        if not os.path.exists(pathToLogFolder):
            print("Директории 'log' не существует! Она будет создана.")
            os.mkdir(pathToLogFolder)

        today = datetime.datetime.today()
        self.pathToNewFolder = os.path.join(pathToLogFolder,
                                  '{}_{}'.format(today.strftime("%Y_%m_%d_%H_%M_%S"), pathToConfigXML[:-4]))
        os.mkdir(self.pathToNewFolder)

        self.logger = logging.getLogger("ETL")
        self.logger.setLevel(logging.DEBUG)

        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)

        pathForLog = os.path.join(self.pathToNewFolder, 'log.txt')
        pathForLog_error = os.path.join(self.pathToNewFolder, 'debug.txt')

        self.fH_errors = logging.FileHandler(pathForLog_error)
        self.sHandler_message = logging.StreamHandler()
        self.fHandler_message = logging.FileHandler(pathForLog)

        self.fHandler_message.setLevel(logging.INFO)
        self.sHandler_message.setLevel(logging.INFO)
        self.fH_errors.setLevel(logging.DEBUG)

        self.sHandler_message.setFormatter(formatter)
        self.fHandler_message.setFormatter(formatter)
        self.fH_errors.setFormatter(formatter)

        self.logger.addHandler(self.sHandler_message)
        self.logger.addHandler(self.fHandler_message)
        self.logger.addHandler(self.fH_errors)


    def deleteLogger(self):
        self.logger.removeHandler(self.sHandler_message)
        self.logger.removeHandler(self.fHandler_message)
        self.logger.removeHandler(self.fH_errors)
