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
Class for Testcases for the codeGrader.backend.db.File Class
@author: mkaiser
"""
import unittest
from codeGrader.backend.db import File, Session
from sqlalchemy import select


class ExerciseTest(unittest.TestCase):
    def test_ExerciseCreation(self):
        """
        Test if the creation of an Exercise in the Database works correctly and if the Exercise can be correctly read from the database
        @return: No return value
        """
        test_file = open("./backend/api_tests/AFileForTesting.txt", 'rb')

        data = {"filename": "AFileForTesting.txt", "fileExtension": ".txt", "file": test_file.read()}
        file = File(**data)
        session = Session()
        session.create(file)
        test_file.close()
        test_file = open("./backend/api_tests/AFileForTesting.txt", 'rb')

        with session.session.begin() as session:
            file_id = session.scalars(select(File.id).where(File.filename == "AFileForTesting.txt")).one()
            file = session.get(File, file_id)
            self.assertEqual(test_file.read(), file.getFileContent())
            self.assertEqual("AFileForTesting.txt", file.filename)
            self.assertEqual(".txt", file.fileExtension)
            session.delete(file)

        test_file.close()
