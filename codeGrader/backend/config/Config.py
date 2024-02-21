# CodeGrader - https://github.com/ooemperor/CodeGrader
# Copyright © 2023, 2024 Michael Kaiser <michael.kaiser@emplabs.ch>
#
# This file is part of CodeGrader.
#
# CodeGrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CodeGrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CodeGrader.  If not, see <http://www.gnu.org/licenses/>.

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
            # For MACOS there might be some changes needed here for the proper file path.
            configFile = os.path.join(os.path.dirname(__file__), "config.conf")
            code = open(os.path.join(os.path.dirname(__file__), "codeLanguages.json"))

        self.config = configparser.ConfigParser()
        self.config.read(configFile)
        codeLanguages = json.load(code)
        code.close()

        self.codeLanguages = codeLanguages

        # Flask Application Configurations
        self.ApiPort = self.config["API"]["Port"]
        self.ApiAddresses = self.config["API"]["Adresses"]
        self.debug = True if self.config["Logging"]["Debug"] == "0" else False
        self.useIntegratedLogin = self.config["Logging"]["UseIntegratedLogging"]
        self.appName = self.config["API"]["Name"]
        self.tokenAuthorization = self.config["API"]["TokenAuthorization"]
        self.tokenLength = int(self.config["API"]["TokenLength"])
        self.cache_bypass = True if self.config["API"]["CacheBypass"] == "1" else False
        self.cache_timeout = int(self.config["API"]["CacheTimeout"])

        # Mail Server Configurations
        self.mail_use_authentication = True if self.config["Mail"]["use_authentication"] == "1" else False
        self.mail_address = self.config["Mail"]["address"]
        self.mail_password = self.config["Mail"]["password"]
        self.mail_smtp = self.config["Mail"]["smtp_server"]
        self.mail_port = self.config["Mail"]["port"]
        self.mail_sender = self.config["Mail"]["sender"]

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
        self.tests_frontendHost = self.config["Tests"]["FrontendHost"]
        self.tests_adminPort = self.config["Tests"]["AdminPort"]
        self.tests_userPort = self.config["Tests"]["UserPort"]

        # Configuration for EvaluationService
        self.evaluationHost = self.config["EvaluationService"]["Host"]
        self.evaluationPort = self.config["EvaluationService"]["Port"]
        self.evaluationIpWhiteList = self.config["EvaluationService"]["IP_Address_Whitelist"]

        # Configuration for the ExecutionService
        self.executionHost = self.config["ExecutionService"]["Host"]
        self.executionPort = self.config["ExecutionService"]["Port"]
        self.executionFilePath = self.config["ExecutionService"]["PathToExecutionFiles"]
        self.executionIpWhiteList = self.config["ExecutionService"]["IP_Address_Whitelist"]
        self.execution_LXC_Install_Command = self.config["ExecutionService"]["LXC_Install_Command"]

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
