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
