"""
Login Page Handler
@author: mkaiser
"""
from flask import request
from .Base import BaseHandler


class LoginHandler(BaseHandler):
    """
    Login Handler for the admin frontend
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the Login Handler
        @param request: The request from the app route of flask
        @type request: flask.request
        """
        super.__init__(request)