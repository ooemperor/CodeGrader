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
Handler for the Password Reset on the User and Admin Objects
@author: mkaiser
"""
import string

import sqlalchemy.exc

from .Base import BaseHandler
from codeGrader.backend.db.Admin import AdminUser
from codeGrader.backend.db.User import User
from sqlalchemy import select
import hashlib
import random


class PasswordResetHandler(BaseHandler):
    """
    Class for the password Reset on the user objects
    Specific User PW Reset Handlers will inherit this class
    """

    def __init__(self) -> None:
        """
        Constructor of the PasswordReset Parent Class.
        Uses the Basehandler
        """
        super().__init__()
        self.password = None
        self.generate_random_password()

    def generate_random_password(self):
        char_list = string.ascii_letters + string.digits + "!-_.?/"
        new_password = ""
        for i in range(10):
            j = random.randint(0, len(char_list) - 1)
            new_password += char_list[j]

        self.password = new_password

    def reset(self, id_: int) -> dict:
        """
        Reset function on the User Object
        @param id_: the id of the user in the database
        @type id_: int
        @return: A Dictionary reporting success or failure
        @rtype: dict
        """
        try:

            self.password = self.password.encode('utf-8')
            self.password = hashlib.sha256(self.password)
            self.password = self.password.hexdigest()

            user = self.sql_session.get_object(self.dbClass, id_)

            user_dict = {"username": user.username, "password": self.password}
            print(self.password)
            self.sql_session.update(self.dbClass, user.id, user_dict)

            return self.create_generic_response('POST', "Password has been reset", password=self.password)

        except Exception as e:
            print(e)
            return self.create_generic_error_response('POST', "Password Reset failed for User")


class AdminUserPasswordResetHandler(PasswordResetHandler):
    """
    Class for the Password Reset Handler of the admin user.
    """

    def __init__(self) -> None:
        """
        Constructor of the AdminUserPasswordResetHandler
        """
        super().__init__()
        self.dbClass = AdminUser


class UserPasswordResetHandler(PasswordResetHandler):
    """
    Class for the Password Reset Handler of the user.
    """

    def __init__(self):
        """
        Constructor of the UserPasswordResetHandler
        """
        super().__init__()
        self.dbClass = User
