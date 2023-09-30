"""
Class for Testcases for the src.backend.db.Task Class
@author: mkaiser
"""
import unittest
from src.backend.db import Task, Session
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
            self.assertEqual(task.name, "task1")
            self.assertEqual(task.tag, "tasktag")
            self.assertEqual(task.id, task_id)
            session.delete(task)
