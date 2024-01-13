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
Class for Testcases for the codeGrader.backend.db.Submission Class
@author: mkaiser
"""
import unittest
from codeGrader.backend.db import Task, Submission, User, Session
from sqlalchemy import select


class SubmissionTest(unittest.TestCase):
    def test_SubmissionCreation(self):
        """
        Test if the creation of a Submission in the Database works correctly and if the Submission can be correctly read from the database
        @return: No return value
        """

        # creating session, user and task that we need in order to test the Submission.
        sql = Session()
        taskdict = {
            "name": "task2",
            "tag": "tasktag"
        }

        task = Task(**taskdict)
        sql.create(task)

        userdict = {
            "username": "tuser1",
            "first_name": "test",
            "last_name": "user",
            "email": "test.user@mail.com",
            "password": "myPassword",
            "tag": "usertag"
        }

        user = User(**userdict)
        sql.create(user)

        # getting the object out of the database
        with sql.session.begin() as session:
            task_id = session.scalars(select(Task.id).where(Task.name == "task2")).one()
            task = session.get(Task, task_id)

            user_id = session.scalars(select(User.id).where(User.username == "tuser1")).one()
            user = session.get(User, user_id)

            submission_dict = dict()
            submission_dict["task_id"] = task.id
            submission_dict["user_id"] = user.id
            submission = Submission(**submission_dict)

            sql.create(submission)
            sub_id = session.scalars(select(Submission.id).where(Submission.task_id == task_id and Submission.user_id == user_id)).one()
            submission = session.get(Submission, sub_id)

            # basic assertions on the submission
            self.assertEqual(user_id, submission.user_id)
            self.assertEqual(task_id, submission.task_id)
            self.assertEqual(user, submission.user)
            self.assertEqual(task, submission.TaskSubmission)

            # testing the correctnes of the user and task that are referenced from the submission
            self.assertEqual("task2", submission.TaskSubmission.name)
            self.assertEqual("tasktag", submission.TaskSubmission.tag)
            self.assertEqual("tuser1", submission.user.username)
            self.assertEqual("test", submission.user.first_name)
            self.assertEqual("user", submission.user.last_name)
            self.assertEqual("usertag", submission.user.tag)

            # deleting the objects after the tests
            session.delete(submission)
            session.delete(task)
            session.delete(user)
