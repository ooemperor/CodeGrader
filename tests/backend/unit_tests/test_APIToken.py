"""
Class for Testcases for the codeGrader.backend.db.Authentication.APIToken Class
@author: mkaiser
"""
import unittest
from codeGrader.backend.db import APIToken, Session
from sqlalchemy import select
import string


class UserTest(unittest.TestCase):

    def test_UserCreation(self):
        """
        Test if the creation of a APIToken in the Database works correctly and if the User can be correctly read from the database
        @return: No return value
        """
        token_description = "Token for testing"

        token = APIToken(token_description)
        session = Session()
        session.create(token)

        with session.session.begin() as session:
            token_id = session.scalars(select(APIToken.id).where(APIToken.description == "Token for testing")).one()
            token = session.get(APIToken, token_id)
            self.assertEqual(30, len(token.token))
            self.assertEqual("Token for testing", token.description)
            self.assertEqual(token_id, token.id)
            for c in token.token:
                self.assertTrue(True if c in (string.ascii_letters + string.digits) else False)
            session.delete(token)
