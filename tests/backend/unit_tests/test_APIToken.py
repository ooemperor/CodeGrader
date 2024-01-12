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
Class for Testcases for the codeGrader.backend.db.Authentication.APIToken Class
@author: mkaiser
"""
import unittest
from codeGrader.backend.db import APIToken, Session
from sqlalchemy import select
import string


class APITokenTest(unittest.TestCase):

    def test_APITokenGeneration(self):
        """
        Test if the creation of a APIToken in the Database works correctly and if the User can be correctly read from the database
        @return: No return value
        """
        token_description = "Token for Unit Tests"

        token = APIToken(token_description)
        session = Session()
        session.create(token)

        with session.session.begin() as session:
            token_id = session.scalars(select(APIToken.id).where(APIToken.description == "Token for Unit Tests")).one()
            token = session.get(APIToken, token_id)
            self.assertEqual(30, len(token.token))
            self.assertEqual("Token for Unit Tests", token.description)
            self.assertEqual(token_id, token.id)
            for c in token.token:
                self.assertTrue(True if c in (string.ascii_letters + string.digits) else False)
            session.delete(token)
