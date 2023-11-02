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
