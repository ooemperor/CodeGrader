"""
Configuration Class for the backend of the CodeGrader
@author: mkaiser
"""
import json
import os


class Config:
    """
    Configuration Class that holds all the necessary configuration and reads them from a json file.
    """

    def __init__(self):
        """
        Init function for the configuration class
        @return: Created Config Object
        """
        f = open(os.path.join(os.path.dirname(__file__), "config.json"))  # TODO Change path to /etc/fileName in productive deployment
        conf = json.load(f)
        f.close()

        self.port = conf["port"]
        self.debug = conf["debug"]
        self.appName = conf["applicationName"]

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
