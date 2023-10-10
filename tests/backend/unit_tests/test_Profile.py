"""
Class for Testcases for the codeGrader.backend.db.Profile Class
@author: mkaiser
"""
import unittest
from codeGrader.backend.db import Profile, Session
from sqlalchemy import select


class ProfileTest(unittest.TestCase):
    def test_ProfileCreation(self):
        """
        Test if the creation of a Profile in the Database works correctly and if the Profile can be correctly read from the database
        @return: No return value
        """
        profile_dict = {
            "name": "TestProfile"
        }
        profile_dict2 = {
            "name": "TestProfile2",
            "tag": "new tag"
        }
        profile = Profile(**profile_dict)
        session = Session()
        session.create(profile)

        with session.session.begin() as session:
            profile_id = session.scalars(select(Profile.id).where(Profile.name == "TestProfile")).one()
            profile = session.get(Profile, profile_id)
            self.assertEqual(profile.name, "TestProfile")
            self.assertEqual(profile.id, profile_id)
            profile.set_attrs(profile_dict2)
            session.commit()

        session = Session()
        with session.session.begin() as session:
            profile2 = session.get(Profile, profile_id)
            self.assertEqual(profile2.name, "TestProfile2")
            self.assertEqual(profile2.tag, "new tag")
            self.assertEqual(profile2.id, profile_id)
            session.delete(profile2)
