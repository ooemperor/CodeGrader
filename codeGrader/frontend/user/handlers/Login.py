"""
Login Page Handler
@author: mkaiser
"""
import flask
from .Base import BaseHandler


class UserLoginHandler(BaseHandler):
    """
    Login Handler for the user frontend
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
        response = self.api.post('/user/login', body)
        id_ = response["response"]["id"] # is None when the Authentication failed
        return id_
