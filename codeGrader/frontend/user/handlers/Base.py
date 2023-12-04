"""
Base Handler for the User part of the CodeGrader Frontend
@author: mkaiser
"""
import flask

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