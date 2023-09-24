"""
Configuration Class for the backend of the CodeGrader
@author: mkaiser
"""
import json


class Config:
    """
    Configuration Class that holds all the necessary configuration and reads them from a json file.
    """

    def __init__(self):
        """
        Init function for the configuration class
        @return: Created Config Object
        """
        f = open("config/config.json")  # TODO Change path to /etc/fileName in productive deployment
        conf = json.load(f)
        f.close()

        self.port = conf["port"]
        self.debug = conf["debug"]
        self.appName = conf["applicationName"]
