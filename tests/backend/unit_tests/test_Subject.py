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
Class for Testcases for the codeGrader.backend.db.Subject Class
@author: mkaiser
"""
import unittest
from codeGrader.backend.db import Subject, Session
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
