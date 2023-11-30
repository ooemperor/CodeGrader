"""
Configuration Class for the backend of the codeGrader
@author: mkaiser
"""
import json
import os
import platform
import configparser


class Config:
    """
    Configuration Class that holds all the necessary configuration and reads them from a json file.
    """

    def __init__(self):
        """
        Init function for the configuration class
        @return: Created Config Object
        """
        self.system = platform.system()
        if self.system == 'Windows':
            configFile = os.path.join(os.path.dirname(__file__), "config.conf")
            code = open(os.path.join(os.path.dirname(__file__), "codeLanguages.json"))
        elif self.system == 'Linux':
            configFile = "/etc/codeGrader/backendConfig.conf"
            code = open("/etc/codeGrader/codeLanguages.json")
        else:
            # For MAC OS there might be some changes needed here for the proper file path.
            configFile = os.path.join(os.path.dirname(__file__), "config.conf")
            code = open(os.path.join(os.path.dirname(__file__), "codeLanguages.json"))

        self.config = configparser.ConfigParser()
        self.config.read(configFile)
        codeLanguages = json.load(code)
        code.close()

        self.codeLanguages = codeLanguages

        # Flask Application Configurations
        self.ApiPort = self.config["API"]["Port"]
        self.debug = self.config["Logging"]["Debug"]
        self.useIntegratedLogin = self.config["Logging"]["UseIntegratedLogging"]
        self.appName = self.config["API"]["Name"]
        self.tokenAuthorization = self.config["API"]["TokenAuthorization"]
        self.tokenLength = int(self.config["API"]["TokenLength"])

        # Configuration for database Connection
        self.DBName = self.config["Database"]["Database"]
        self.DBUser = self.config["Database"]["Username"]
        self.DBPassword = self.config["Database"]["Password"]
        self.DBHost = self.config["Database"]["Host"]
        self.DBPort = self.config["Database"]["Port"]
        self.dbConnectionString = (self.config["Database"]["Dialect"] +
                                   "+" +
                                   self.config["Database"]["DBDriver"] +
                                   "://" +
                                   self.config["Database"]["Username"] +
                                   ":" +
                                   self.config["Database"]["Password"] +
                                   "@" +
                                   self.config["Database"]["Host"] +
                                   ":" +
                                   self.config["Database"]["Port"] +
                                   "/" +
                                   self.config["Database"]["Database"]
                                   )
        self.metadataColumnsAmount = self.config["Database"]["MetaDataColumnsCount"]
        self.columnIgnoreList = self.config["Database"]["ColumnIgnoreList"]

        # Configurations for Testing purposes
        self.tests_ApiHost = self.config["Tests"]["ApiHost"]
        self.tests_ApiPort = self.ApiPort

        # Configuration for EvaluationService
        self.evaluationHost = self.config["EvaluationService"]["Host"]
        self.evaluationPort = self.config["EvaluationService"]["Port"]

        # Configuration for the ExecutionService
        self.executionHost = self.config["ExecutionService"]["Host"]
        self.executionPort = self.config["ExecutionService"]["Port"]
        self.executionFilePath = self.config["ExecutionService"]["PathToExecutionFiles"]

    def getInstallationCommand(self, codeLanguage: str):
        """
        Getting the installation command for a given Programming language
        @param codeLanguage: The name of the programming language
        @type codeLanguage: str
        @return: The Installation Command that needs to be executed in order to be able to run the codeLanguage in the LXC
        @rtype: str
        """
        return self.codeLanguages["codeLanguages"][codeLanguage]["installationCommand"]

    def getExecutionCommand(self, codeLanguage: str):
        """
        Getting the execution command for the given codeLanguage
        @param codeLanguage: The name of the programming language
        @type codeLanguage: str
        @return: The RunTime Command that needs to be executed in order to be able to run the codeLanguage in the LXC
        @rtype: str
        """
        return self.codeLanguages["codeLanguages"][codeLanguage]["runCommand"]