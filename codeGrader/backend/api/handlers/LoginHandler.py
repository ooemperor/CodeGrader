"""
Handler for the Login
@author: mkaiser
"""
import sqlalchemy.exc

from .Base import BaseHandler
from codeGrader.backend.db.Admin import AdminUser
from .Exceptions import AuthorizationException
from sqlalchemy import select
import hashlib


class AdminUserLoginHandler(BaseHandler):
    """
    Class for the login Handler
    Used by the frontend to check the login status of a AdminUser.
    """

    def __init__(self):
        """
        Constructor of the
        """
        super().__init__()
        self.dbClass = AdminUser

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
        try:
            with self.sql_session.session.begin() as session:
                adminUser_id = session.scalars(select(AdminUser.id).where(AdminUser.username == username)).one()

            user = self.sql_session.get_object(AdminUser, adminUser_id)
            password = password.encode('utf-8')
            password = hashlib.sha256(password)
            password = password.hexdigest()
            if user.username == username and user.password == password:
                return self.create_generic_response('GET', "Authentication successful for User", user.id)
            else:
                return self.create_generic_response('GET', "Authentication failed for User")

        except sqlalchemy.exc.NoResultFound as err:
            # incase we do not find a user with the given credentials
            return self.create_generic_response('GET', "Authentication failed for User")
