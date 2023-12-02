"""
Config Class for the frontend of the codeGrader
@author: mkaiser
"""

import json
import os
import platform
import configparser


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
            configFile = os.path.join(os.path.dirname(__file__), "config.conf")
            self.templatesDir = os.path.abspath('./templates')
        elif self.system == 'Linux':
            configFile = "/etc/codeGrader/frontendConfig.conf"
            self.templatesDir = './templates'
        else:
            # For MAC OS there might be some changes needed here for the proper file path.
            configFile = os.path.join(os.path.dirname(__file__), "config.conf")

        self.config = configparser.ConfigParser()
        self.config.read(configFile)
        print(self.config.sections())


        self.adminPort = self.config["Admin"]["Port"]
        self.adminAppName = self.config["Admin"]["Name"]
        self.adminSecretKey = self.config["Admin"]["Secret_Key"]

        self.userPort = self.config["User"]["Port"]
        self.userAppName = self.config["User"]["Name"]
        self.userSecretKey = self.config["User"]["Secret_Key"]

        self.apiHost = self.config["API"]["Host"]
        self.apiPort = self.config["API"]["Port"]
        self.apiAuthentication = self.config["API"]["Authentication_Type"]
        self.apiToken = self.config["API"]["Authentication_Token"]
