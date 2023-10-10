"""
Class for Testcases for the codeGrader.backend.db.Exercise Class
@author: mkaiser
"""
import unittest
from codeGrader.backend.db import Exercise, Session
from sqlalchemy import select


class ExerciseTest(unittest.TestCase):
    def test_ExerciseCreation(self):
        """
        Test if the creation of an Exercise in the Database works correctly and if the Exercise can be correctly read from the database
        @return: No return value
        """
        exercisedict = {
            "name": "exercise1",
            "tag": "exercisetag"
        }

        exercise = Exercise(**exercisedict)
        session = Session()
        session.create(exercise)

        with session.session.begin() as session:
            exercise_id = session.scalars(select(Exercise.id).where(Exercise.name == "exercise1")).one()
            exercise = session.get(Exercise, exercise_id)
            self.assertEqual(exercise.name, "exercise1")
            self.assertEqual(exercise.tag, "exercisetag")
            self.assertEqual(exercise.id, exercise_id)
            session.delete(exercise)
