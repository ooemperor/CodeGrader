"""
Class for Testcases for the src.backend.db.Subject Class
@author: mkaiser
"""
import unittest
from src.backend.db import Subject, Session
from sqlalchemy import select


class SubjectTest(unittest.TestCase):
    def test_SubjectCreation(self):
        """
        Test if the creation of a Subject in the Database works correctly and if the Subject can be correctly read from the database
        @return: No return value
        """
        subjectdict = {
            "name": "subject1",
            "tag": "subjecttag"
        }

        subject = Subject(**subjectdict)
        session = Session()
        session.create(subject)

        with session.session.begin() as session:
            subject_id = session.scalars(select(Subject.id).where(Subject.name == "subject1")).one()
            subject = session.get(Subject, subject_id)
            self.assertEqual(subject.name, "subject1")
            self.assertEqual(subject.tag, "subjecttag")
            self.assertEqual(subject.id, subject_id)
            session.delete(subject)
