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
Class for Testcases for the codeGrader.backend.db.Task Class
@author: mkaiser
"""
import unittest
from codeGrader.backend.db import Task, Session
from sqlalchemy import select


class TaskTest(unittest.TestCase):
    def test_TaskCreation(self):
        """
        Test if the creation of a Task in the Database works correctly and if the Task can be correctly read from the database
        @return: No return value
        """
        taskdict = {
            "name": "task1",
            "tag": "tasktag"
        }

        task = Task(**taskdict)
        session = Session()
        session.create(task)

        with session.session.begin() as session:
            task_id = session.scalars(select(Task.id).where(Task.name == "task1")).one()
            task = session.get(Task, task_id)
            self.assertEqual("task1", task.name )
            self.assertEqual("tasktag", task.tag)
            self.assertEqual( task_id, task.id)
            session.delete(task)
