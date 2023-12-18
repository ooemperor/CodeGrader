"""
Base Handler for the User part of the CodeGrader Frontend
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

    def __init__(self, requests: flask.Request):
        """
        Constructor of the BaseHandler
        """
        self.request = requests
        self.api = ApiHandler(config.apiHost, config.apiAuthentication, config.apiToken)
        self.user = flask_login.current_user

    def get_value(self, value: str, default: str = ""):
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
