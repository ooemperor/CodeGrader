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
        elif self.system == 'Linux':
            configFile = open("/etc/codeGrader/frontendConfig.json")
        else:
            # For MAC OS there might be some changes needed here for the proper file path.
            configFile = open(os.path.join(os.path.dirname(__file__), "config.json"))

        conf = json.load(configFile)
        configFile.close()

        self.adminPort = conf["admin"]["port"]
        self.adminAppName = conf["admin"]["applicationName"]

        self.userPort = conf["user"]["port"]
        self.userAppName = conf["user"]["applicationName"]

        self.apiHost = conf["api"]["host"]
        self.apiPort = conf["api"]["port"]
        self.apiToken = conf["api"]["token"]