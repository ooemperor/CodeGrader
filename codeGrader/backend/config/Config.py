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
            f = open(os.path.join(os.path.dirname(__file__), "config.json"))
        elif self.system == 'Linux':
            f = open("/etc/codeGrader/config.json")
        else:
            # For MAC OS there might be some changes needed here for the proper file path.
            f = open(os.path.join(os.path.dirname(__file__), "config.json"))

        conf = json.load(f)
        f.close()

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
