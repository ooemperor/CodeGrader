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
Class for Testcases for the codeGrader.backend.db.User Class
@author: mkaiser
"""
import unittest
from codeGrader.backend.db import AdminUser, User, Session
from sqlalchemy import select


class UserTest(unittest.TestCase):

    def test_UserCreation(self):
        """
        Test if the creation of a User in the Database works correctly and if the User can be correctly read from the database
        @return: No return value
        """
        userdict = {
            "username": "tuser",
            "first_name": "test",
            "last_name": "user",
            "email": "test.user@mail.com",
            "password": "myPassword",
            "tag": "usertag"
        }

        user = User(**userdict)
        session = Session()
        session.create(user)

        with session.session.begin() as session:
            user_id = session.scalars(select(User.id).where(User.username == "tuser")).one()
            user = session.get(User, user_id)
            self.assertEqual(user.username, "tuser")
            self.assertEqual(user.first_name, "test")
            self.assertEqual(user.last_name, "user")
            self.assertEqual(user.email, "test.user@mail.com")
            self.assertEqual(user.password, "myPassword")
            self.assertEqual(user.tag, "usertag")
            self.assertEqual(user.id, user_id)
            session.delete(user)

    def test_AdminUserCreation(self):
        """
        Test if the creation of a AdminUser in the Database works correctly and if the AdminUser can be correctly read from the database
        @return: No return value
        """
        adminuserdict = {
            "username": "auser",
            "first_name": "admin",
            "last_name": "user",
            "email": "admin.user@mail.com",
            "password": "myPassword",
            "tag": "adminUserTag",
            "admin_type": 1
        }

        adminuser = AdminUser(**adminuserdict)
        session = Session()
        session.create(adminuser)

        with session.session.begin() as session:
            adminuser_id = session.scalars(select(AdminUser.id).where(AdminUser.username == "auser")).one()
            adminuser = session.get(AdminUser, adminuser_id)
            self.assertEqual(adminuser.username, "auser")
            self.assertEqual(adminuser.first_name, "admin")
            self.assertEqual(adminuser.last_name, "user")
            self.assertEqual(adminuser.email, "admin.user@mail.com")
            self.assertEqual(adminuser.password, "myPassword")
            self.assertEqual(adminuser.tag, "adminUserTag")
            self.assertEqual(adminuser.id, adminuser_id)
            session.delete(adminuser)
