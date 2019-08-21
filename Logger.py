import datetime
import logging
import os
from string import Template

class Log_info:
    __instance = None
    __config = None

    @classmethod
    def getInstance(cls, pathToConfigXML, configs_list):
        if not cls.__instance:
            cls.__instance = Log_info(pathToConfigXML, configs_list)
        return cls.__instance

    def set_config(self, pathToConfigXML):
        if not self.__config:
            self.__config = pathToConfigXML
        elif self.__config != pathToConfigXML:
            self.__config = pathToConfigXML

    def __init__(self, pathToConfigXML, configs_list):
        self.getLogger(configs_list)
        self.set_config(pathToConfigXML)

    def getLogger(self, configs_list):
        currentPath = os.getcwd()
        pathToLogFolder = os.path.join(currentPath, 'log')  # folder log
        if not os.path.exists(pathToLogFolder):
            print("Creating dir <log>")
            os.mkdir(pathToLogFolder)

        today = datetime.datetime.today()
        self.pathToNewFolder = os.path.join(pathToLogFolder,
                                  '{}_{}'.format(today.strftime("%Y_%m_%d_%H_%M_%S"), configs_list))
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

    def raiseError(self, errNum, *message):
        message_temp = "default_error"
        t = Template('Error <$num> - $message')

        dict_of_err_types = {
            0: "Unknown error",
            1: "Error at parsing XML",
            2: "Error at DB connection",
            3: "Validate error",
            4: "Query creating error"
        }

        if errNum == 0:
            message_temp = f"""{dict_of_err_types.get(0)}: Message - <{message[0]}>"""
        if errNum == 1:
            message_temp = f"""{dict_of_err_types.get(1)}: Message - <{message[0]}>"""
        if errNum == 2:
            message_temp = f"""{dict_of_err_types.get(1)}: Cant find file XML <{message[0]}>\nMessage - {message[1]}"""
        if errNum == 3:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find tag <{message[0]}> in <{self.__config}>"""
        if errNum == 4:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find option <--{message[0]}> in command line"""
        if errNum == 5:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find tag <{message[0]}> in <column> tag at block number <{message[1] + 1}> in <importXml/columns> block in <{self.__config}>"""
        if errNum == 6:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find property mode in tag <{message[0]}> in <column> tag at block number <{message[1] + 1}> in <importXml/columns> block in <{self.__config}>"""
        if errNum == 7:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find property mode in tag <{message[0]}> in <replace> tag at block number <{message[1]}> in <importXml/columns> block in <{self.__config}>"""
        if errNum == 8:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find property mode in tag <{message[0]}> in <{self.__config}>""",
        if errNum == 9:
            message_temp = f"""{dict_of_err_types.get(1)}: <--check_mode true>. if you want to check source file you must to set <linkedColumns mode="true">"""
        if errNum == 10:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find tag <{message[0]}> in <importXml/linkedColumns> tag at block number <{message[1]}> in <{self.__config}>"""
        if errNum == 11:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find tag <{message[0]}> in <column> tag at block number <{message[1]}> in <importXml/withDict> block in <{self.__config}>"""
        if errNum == 12:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find property mode in tag <{message[0]}> in <column> tag at block number <{message[1]}> in <importXml/withDict> block in <{self.__config}>"""
        if errNum == 13:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find property mode in tag <{message[0]}> in <replace> tag at block number <{message[1]}> in <importXml/withDict> block in <{self.__config}>"""
        if errNum == 14:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find tag <{message[0]}> in <column> tag at block number <{message[1]}> in <exportTable/columns> block in <{self.__config}>"""
        if errNum == 15:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find property mode in tag <{message[0]}> in <column> tag at block number <{message[1]}> in <exportTable/columns> block in <{self.__config}>"""
        if errNum == 16:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't open excel file on path: <{message[0]}> on page: <{message[1]}> - \nSystem message: <{message[2]}>"""
        if errNum == 17:
            message_temp = f"""{dict_of_err_types.get(1)}: Can't find tag <colName> for tag <colNameInSource> from tag <linkedColumns>"""
        if errNum == 18:
            message_temp = f"""{dict_of_err_types.get(2)}: Fail to connect to <{message[0]}> <{message[1]}> <{message[2]}> <{message[3]}>"""
        if errNum == 19:
            message_temp = f"""{dict_of_err_types.get(2)}: Fail to close connection"""
        if errNum == 20:
            message_temp = f"""{dict_of_err_types.get(3)}: Error in exec query in validate operation\nSystem message:<{message[0]}>"""
        if errNum == 21:
            message_temp = f"""{dict_of_err_types.get(3)}: In table <{message[0]}> value <{message[1]}> in column <{message[2]}> is not exists in column <{message[3]}> in table <{message[4]}> at list <{message[5]}>"""
        if errNum == 22:
            message_temp = f"""{dict_of_err_types.get(3)}: In tag <exportTable> in column number <{message[0]}> column property <fromDb>true</fromDb> but <withDict mode="false">"""
        if errNum == 23:
            message_temp = f"""{dict_of_err_types.get(3)}: Mode <dict>true<dict> but in tag <dbColumns> no column property <fromDb>true</fromDb>"""
        if errNum == 24:
            message_temp = f"""{dict_of_err_types.get(3)}: In tag <withDict> in column number <{message[0]}> tag <colNameDb> == <None>"""
        if errNum == 25:
            message_temp = f"""{dict_of_err_types.get(3)}: In tag <withDict> in column number <{message[0]}> tag <colName> == <None>"""
        if errNum == 26:
            message_temp = f"""{dict_of_err_types.get(3)}: Column <{message[0]}> in file <{message[1]}> at list <{message[2]}> contains <Null> but column not <Null>"""
        if errNum == 27:
            message_temp = f"""{dict_of_err_types.get(3)}: Value <{message[0]}> in column <{message[1]}> in file <{message[2]}> at list <{message[3]}> is not unique"""
        if errNum == 28:
            message_temp = f"""{dict_of_err_types.get(3)}: Column: <{message[0]}> not exists in <{message[1]}> on list <{message[2]}>. You must chose from this names: <{message[3]}>"""
        if errNum == 29:
            message_temp = f"""{dict_of_err_types.get(3)}: Columns: <{message[0]}> not exists in <exportTable/columns> list in config"""
        if errNum == 30:
            message_temp = f"""{dict_of_err_types.get(3)}: Columns: <{message[0]}> not exists in table <{message[1]}>; In DB: <{message[2]}>. Set of columns in db table:\n<{message[3]}>"""
        if errNum == 31:
            message_temp = f"""{dict_of_err_types.get(3)}: Columns: <{message[0]}> not exists in <importXml/columns/column/colNameDb> tag in the <{message[1]}> file configuration.\nList of exists columns in that tag: <{message[2]}>"""
        if errNum == 32:
            message_temp = f"""{dict_of_err_types.get(3)}: Columns: <{message[0]}> not exists in linked table.List of exists columns in that tag: <{message[1]}>"""
        if errNum == 33:
            message_temp = f"""{dict_of_err_types.get(3)}: Columns: <{message[0]}> not exists in source table.List of exists columns in that tag: <{message[1]}>"""
        if errNum == 34:
            message_temp = f"""{dict_of_err_types.get(3)}: Option <--test_mode> don't selected"""
        if errNum == 35:
            message_temp = f"""{dict_of_err_types.get(1)}: Message - \n<{message[0]}>"""
        if errNum == 36:
            message_temp = f"""{dict_of_err_types.get(4)}: Can't concatenate <int>"""
        if errNum == 37:
            message_temp = f"""{dict_of_err_types.get(2)}: Can't find table <{message[0]}> in data base."""
        if errNum == 38:
            message_temp = f"""{dict_of_err_types.get(2)}: Message - \n<{message[0]}>"""
        if errNum == 39:
            message_temp = f"""{dict_of_err_types.get(0)}: Can't create dictionary data frame. Message - <{message[0]}>"""
        if errNum == 40:
            message_temp = f"""{dict_of_err_types.get(1)}: In tag <{message[0]}>. Value <{message[1]}> in column number <{message[2] + 1}> not <int> type"""
        if errNum == 41:
            message_temp = f"""{dict_of_err_types.get(3)}: At <exportTable/columns> tag in column number <{message[0]}> in <name>{message[1]}<name> incompatible set of attributes"""

        self.logger.error(t.substitute(num=errNum, message=message_temp))
        raise SystemExit(1)


    def raiseInfo(self, info_num, *message):
        message_temp = "default_info"
        t = Template("$message")


        if info_num == 0:
            message_temp = f"Success"
        if info_num == 1:
            message_temp = f"""Success open excel file: <{message[0]}> on page name: <{message[1]}>, list number: <{message[2] + 1}>"""
        if info_num == 2:
            message_temp = f"""Success connection to host: <{message[0]}>, port: <{message[1]}>, database name: <{message[2]}>"""
        if info_num == 3:
            message_temp = f"""Connection to DB closed"""
        if info_num == 4:
            message_temp = f"""Starts executing... {self.__config}"""
        if info_num == 5:
            message_temp = f"""Begin validating files..."""
        if info_num == 6:
            message_temp = f"""Validate success..."""
        if info_num == 7:
            message_temp = f"""Ends executing... successfully completed <{self.__config}>\n---"""
        if info_num == 8:
            message_temp = f"""Loading in db begin..."""
        if info_num == 9:
            message_temp = f"""Test mode: <{message[0]}>"""
        if info_num == 10:
            message_temp = f"""Rows readed: {message[0]}%"""
        if info_num == 11:
            message_temp = f"""Created <{message[0]}> test queries"""
        if info_num == 12:
            message_temp = f"""Inserted: <{message[0]}>; Rows lost: <{message[1]}>"""
        if info_num == 13:
            message_temp = f"""Log files created in: <{message[0]}>"""
        if info_num == 14:
            message_temp = f"""Reconnect in: <{message[0]}> minute"""
        if info_num == 15:
            message_temp = f"""Connection to DB lost... Message - \n<{message[0]}>"""
        if info_num == 16:
            message_temp = f"""Attempt - <{message[0]}>"""

        self.logger.info(t.substitute(message=message_temp))

    def raiseDebug(self,debug_num, *message):
        message_temp = "default_debug"
        t = Template("Debug <$number> - $message")

        if debug_num == 0:
            message_temp = f""" - {message[0]}"""
        if debug_num == 1:
            message_temp = f"""Error in database while commiting query:\nRow number:<{message[0]}>\nQuery: 
                            <{message[1]}>\nMessage - \n<{message[2]}>\n"""

        self.logger.debug(t.substitute(number=debug_num, message=message_temp))


