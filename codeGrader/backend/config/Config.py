"""
Configuration Class for the backend of the codeGrader
@author: mkaiser
"""
import json
import os
import platform


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
            configFile = open(os.path.join(os.path.dirname(__file__), "config.json"))
            code = open(os.path.join(os.path.dirname(__file__), "codeLanguages.json"))
        elif self.system == 'Linux':
            configFile = open("/etc/codeGrader/backendConfig.json")
            code = open("/etc/codeGrader/codeLanguages.json")
        else:
            # For MAC OS there might be some changes needed here for the proper file path.
            configFile = open(os.path.join(os.path.dirname(__file__), "config.json"))
            code = open(os.path.join(os.path.dirname(__file__), "codeLanguages.json"))

        conf = json.load(configFile)
        codeLanguages = json.load(code)
        configFile.close()
        code.close()

        self.codeLanguages = codeLanguages

        # Flask Application Configurations
        self.ApiPort = conf["api"]["port"]
        self.debug = conf["logging"]["debug"]
        self.useIntegratedLogin = conf["logging"]["useIntegratedLogging"]
        self.appName = conf["api"]["applicationName"]
        self.tokenAuthorization = conf["api"]["TokenAuthorization"]
        self.tokenLength = conf["api"]["tokenLength"]

        # Configuration for database Connection
        self.DBName = conf["database"]["database"]
        self.DBUser = conf["database"]["username"]
        self.DBPassword = conf["database"]["password"]
        self.DBHost = conf["database"]["host"]
        self.DBPort = conf["database"]["port"]
        self.dbConnectionString = (conf["database"]["dialect"] +
                                   "+" +
                                   conf["database"]["DBdriver"] +
                                   "://" +
                                   conf["database"]["username"] +
                                   ":" +
                                   conf["database"]["password"] +
                                   "@" +
                                   conf["database"]["host"] +
                                   ":" +
                                   conf["database"]["port"] +
                                   "/" +
                                   conf["database"]["database"]
                                   )
        self.metadataColumnsAmount = conf["database"]["datamodel"]["metadataColumnsCount"]
        self.columnIgnoreList = conf["database"]["datamodel"]["columnIgnoreList"]

        # Configurations for Testing purposes
        self.tests_ApiHost = conf["tests"]["apiHost"]
        self.tests_ApiPort = self.ApiPort

        # Configuration for EvaluationService
        self.evaluationHost = conf["evaluationService"]["host"]
        self.evaluationPort = conf["evaluationService"]["port"]

        # Configuration for the ExecutionService
        self.executionHost = conf["executionService"]["host"]
        self.executionPort = conf["executionService"]["port"]
        self.executionFilePath = conf["executionService"]["PathToExecutionFiles"]

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