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

import unittest
import requests, json
from codeGrader.backend.config import config
from codeGrader.frontend.config import config as api_config


class ApiTaskTest(unittest.TestCase):

    def setUp(self):
        self.headers = dict()
        self.headers["Authorization"] = f"{api_config.apiAuthentication} {api_config.apiToken}"

    def test_createAndDeleteTask(self):
        """
        Test Case for creating and deleting the Task.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/task/add"
        task_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/task/"

        task_dict = {
            "name": "testTask",
            "tag": "tasktag",
            "description": "Test Description"
        }
        r = requests.post(create_url, json=task_dict, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        task_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{task_url}{task_id}", headers=self.headers)
        self.assertEqual(200, r.status_code)
        self.assertEqual("testTask", json.loads(r.text)["name"])
        self.assertEqual("tasktag", json.loads(r.text)["tag"])
        self.assertEqual(None, json.loads(r.text)["attachments"])
        self.assertEqual(None, json.loads(r.text)["instructions"])
        self.assertEqual("Test Description", json.loads(r.text)["description"])

        r = requests.delete(f"{task_url}{task_id}", headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(204, r.status_code)

    def test_createUpdateAndDeleteTask(self):
        """
        Test Case for creating and deleting the Task.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/task/add"
        task_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/task/"

        task_dict = {
            "name": "testTask",
            "tag": "tasktag",
            "description": "Test Description"
        }

        task_dict_2 = {
            "name": "newTaskName",
            "tag": "newTag",
            "description": "Test Description New"
        }
        r = requests.post(create_url, json=task_dict, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        task_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{task_url}{task_id}", headers=self.headers)
        self.assertEqual(200, r.status_code)
        self.assertEqual(task_id, json.loads(r.text)["id"])
        self.assertEqual("testTask", json.loads(r.text)["name"])
        self.assertEqual("tasktag", json.loads(r.text)["tag"])
        self.assertEqual(None, json.loads(r.text)["attachments"])
        self.assertEqual(None, json.loads(r.text)["instructions"])
        self.assertEqual("Test Description", json.loads(r.text)["description"])

        r = requests.put(f"{task_url}{task_id}", json=task_dict_2, headers={'content-type': 'application/json',
                                                                            'Authorization': f"{api_config.apiAuthentication} {api_config.apiToken}"})
        self.assertEqual(200, r.status_code)

        r = requests.get(f"{task_url}{task_id}", headers=self.headers)
        self.assertEqual(task_id, json.loads(r.text)["id"])
        self.assertEqual("newTaskName", json.loads(r.text)["name"])
        self.assertEqual("newTag", json.loads(r.text)["tag"])
        self.assertEqual(None, json.loads(r.text)["attachments"])
        self.assertEqual(None, json.loads(r.text)["instructions"])
        self.assertEqual("Test Description New", json.loads(r.text)["description"])

        r = requests.delete(f"{task_url}{task_id}", headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(204, r.status_code)

    def test_GETTasksEndpoint(self):
        """
        Test Case for the testing if the /tasks endpoint is working
        @return: No return
        """
        url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/tasks"

        r = requests.get(url, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(json.loads(r.text)["task"])
