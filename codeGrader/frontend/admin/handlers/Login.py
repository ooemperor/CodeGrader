"""
Login Page Handler
@author: mkaiser
"""
import flask
import json
from .Base import BaseHandler


class AdminUserLoginHandler(BaseHandler):
    """
    Login Handler for the admin frontend
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the AdminUser Login Handler
        @param request: The request from the app route of flask
        @type request: flask.request
        """
        super().__init__(request)

    def post(self):
        """
        Trying the authentication of the AdminUser via BackendAPI
        @return: User id_ if the credentials have been correct
        @rtype: int
        """

        username = self.request.form["username"]
        password = self.request.form["password"]
        body = dict()
        body["password"] = password
        body["username"] = username
        response = self.api.post('/login', body)
        id_ = json.loads(response)["response"]["id"]
        return id_
