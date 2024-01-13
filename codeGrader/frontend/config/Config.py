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
            configFile = os.path.join(os.path.dirname(__file__), "config.sec.conf")
            self.templatesDir = os.path.abspath('./templates')
        elif self.system == 'Linux':
            configFile = "/etc/codeGrader/frontendConfig.conf"
            self.templatesDir = './templates'
        else:
            # For MAC OS there might be some changes needed here for the proper file path.
            configFile = os.path.join(os.path.dirname(__file__), "config.conf")

        self.config = configparser.ConfigParser()
        self.config.read(configFile)


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

        self.admin_rw_full = self.config["AdminTypes"]["rwFull"]
        self.admin_rw_partial = self.config["AdminTypes"]["rwPartial"]
        self.admin_r_full = self.config["AdminTypes"]["rFull"]
        self.admin_r_partial = self.config["AdminTypes"]["rPartial"]
