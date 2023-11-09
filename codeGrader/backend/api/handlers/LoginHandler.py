"""
Handler for the Login
@author: mkaiser
"""

from .Base import BaseHandler
from codeGrader.backend.db.User import User
from .Exceptions import AuthorizationException
from sqlalchemy import select


class LoginHandler(BaseHandler):
    """
    Class for the login Handler
    Used by the frontend to check the login status of a user.
    """

    def __init__(self):
        """
        Constructor of the
        """
        super().__init__()
        self.dbClass = User

    def login(self, username: str, password: str):
        """
        Verifying if a user provided the correct login credentials
        @param username: The username of the user
        @type username: str
        @param password: The password of the user
        @type password: str
        @return: Generic Response that gets generated.
        @rtype: dict
        """
        user_id = self.sql_session.session.begin().scalars(select(User.id).where(User.username == username)).one()
        user = self.sql_session.get_object(User, user_id)
        if user.username == username and user.password == password:
            return self.create_generic_response('GET', "Authentication successful for User", user.id)
        else:
            return self.create_generic_response('GET', "Authentication failed for User")

