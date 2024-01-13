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
Base Handler for the admin part of the CodeGrader Frontend
@author: mkaiser
"""
import flask
import flask_login
from flask import flash

from codeGrader.frontend.config import config
from codeGrader.frontend.util import ApiHandler


class BaseHandler:
    """
    Base Handler Class
    Other Handlers will inherit from this class
    """

    def __init__(self, requests: flask.Request) -> None:
        """
        Constructor of the BaseHandler
        """
        self.request: requests = requests
        self.api: ApiHandler = ApiHandler(config.apiHost, config.apiAuthentication, config.apiToken)
        self.admin = flask_login.current_user

    def get_value(self, value: str, default: str = "") -> str:
        """
        Get a value from the form that has been provided by the user identified by a given key.
        The key is defined by the name in the html form
        @param value: Name of the object in the request
        @type value: str
        @param default: The default value that shall be returned when no value is found. Optional parameter
        @type default: str
        @return: The value of the requested key
        @rtype: str
        """
        try:
            value = self.request.form[value]
            if value == '':
                return None
            else:
                return value
        except Exception as err:
            print(err)
            return default

    @staticmethod
    def flash(message: str, severity: str = None) -> None:
        """
        Flashing a message in the rendered HTML Template
        This function will be used further to track the errors
        @param message: The message to be flashed
        @type message: str
        @param severity: The severity of the flash
        @return: No Return made
        @rtype: None
        """
        flash(message, severity)