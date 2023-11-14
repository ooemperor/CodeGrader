"""
Config Class for the frontend of the codeGrader
@author: mkaiser
"""

import json
import os
import platform


class Config:
    """
    Config class for the Frontend of the codeGrader
    """
    def __init__(self):
        """
        init Method to load all the needed values
        @return: the config object
        """

        self.system = platform.system()
        if self.system == 'Windows':
            configFile = open(os.path.join(os.path.dirname(__file__), "config.json"))
            self.templatesDir = os.path.abspath('./templates')
        elif self.system == 'Linux':
            configFile = open("/etc/codeGrader/frontendConfig.json")
            self.templatesDir = './templates'
        else:
            # For MAC OS there might be some changes needed here for the proper file path.
            configFile = open(os.path.join(os.path.dirname(__file__), "config.json"))

        conf = json.load(configFile)
        configFile.close()

        self.adminPort = conf["admin"]["port"]
        self.adminAppName = conf["admin"]["applicationName"]
        self.adminSecretKey = conf["admin"]["secret_key"]

        self.userPort = conf["user"]["port"]
        self.userAppName = conf["user"]["applicationName"]
        self.userSecretKey = conf["user"]["secret_key"]

        self.apiHost = conf["api"]["host"]
        self.apiPort = conf["api"]["port"]
        self.apiAuthentication = conf["api"]["authentication_type"]
        self.apiToken = conf["api"]["authentication_token"]
