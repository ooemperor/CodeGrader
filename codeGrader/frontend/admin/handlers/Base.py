"""
Base Handler for the admin part of the CodeGrader Frontend
@author: mkaiser
"""
from codeGrader.frontend.config import config
from flask import request


class BaseHandler:
    """
    Base Handler Class
    Other Handlers will inherit from this class
    """

    def __init__(self, request):
        """
        Constructor of the BaseHandler
        """
        self.request = request
        # self.apiRequest = ''

    def get_value(self, value: str):
        """
        Get a value from the form that has been provided by the user identified by a given key.
        The key is defined by the name in the html form
        @param value: Name of the object in the request
        @type value: str
        @return: The value of the requested key
        @rtype: str
        """
        try:
            return self.request.form[value]
        except Exception as err:
            print(err)
            return ''  # TODO: check if this makes sense.
