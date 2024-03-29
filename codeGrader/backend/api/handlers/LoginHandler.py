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
Handler for the Login
@author: mkaiser
"""
import sqlalchemy.exc

from .Base import BaseHandler
from codeGrader.backend.db.Admin import AdminUser
from codeGrader.backend.db.User import User
from .Exceptions import AuthorizationException
from sqlalchemy import select
import hashlib


class LoginHandler(BaseHandler):
    """
    Class for the login Handler
    Specific User Login Handlers will then inherit from this class.
    Used by the frontend to check the login status of a AdminUser.
    """

    def __init__(self) -> None:
        """
        Constructor of the LoginHandler Parent Class.
        Uses the Basehandler
        """
        super().__init__()

    def login(self, username: str, password: str) -> dict:
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
                user_id = session.scalars(select(self.dbClass.id).where(self.dbClass.username == username)).one()

            user = self.sql_session.get_object(self.dbClass, user_id)
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


class AdminUserLoginHandler(LoginHandler):
    """
    Class for the login Handler
    Used by the frontend to check the login status of a AdminUser.
    """

    def __init__(self) -> None:
        """
        Constructor of the AdminUserLoginHandler
        """
        super().__init__()
        self.dbClass = AdminUser


class UserLoginHandler(LoginHandler):
    """
    Class for the Login Handler of a normal user.
    Used in frontend to check the login status of a normal User
    """

    def __init__(self):
        """
        Constructor of the
        """
        super().__init__()
        self.dbClass = User
