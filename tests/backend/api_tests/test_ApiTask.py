import unittest
import requests, json
from codeGrader.backend.config import config


class ApiTaskTest(unittest.TestCase):
    def test_createAndDeleteTask(self):
        """
        Test Case for creating and deleting the Task.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/addTask"
        task_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/task/"

        task_dict = {
            "name": "testTask",
            "tag": "tasktag"
        }
        r = requests.post(create_url, json=task_dict)
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        task_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{task_url}{task_id}")
        self.assertEqual(200, r.status_code)
        self.assertEqual("testTask", json.loads(r.text)["name"])
        self.assertEqual("tasktag", json.loads(r.text)["tag"])
        self.assertEqual(None, json.loads(r.text)["attachments"])
        self.assertEqual(None, json.loads(r.text)["instructions"])

        r = requests.delete(f"{task_url}{task_id}")
        self.assertIsNotNone(r)
        self.assertEqual(204, r.status_code)

    def test_createUpdateAndDeleteTask(self):
        """
        Test Case for creating and deleting the Task.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/addTask"
        task_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/task/"

        task_dict = {
            "name": "testTask",
            "tag": "tasktag"
        }

        task_dict_2 = {
            "name": "newTaskName",
            "tag": "newTag"
        }
        r = requests.post(create_url, json=task_dict)
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        task_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{task_url}{task_id}")
        self.assertEqual(200, r.status_code)
        self.assertEqual(task_id, json.loads(r.text)["id"])
        self.assertEqual("testTask", json.loads(r.text)["name"])
        self.assertEqual("tasktag", json.loads(r.text)["tag"])
        self.assertEqual(None, json.loads(r.text)["attachments"])
        self.assertEqual(None, json.loads(r.text)["instructions"])

        r = requests.put(f"{task_url}{task_id}", json=task_dict_2, headers={'content-type': 'application/json'})
        self.assertEqual(200, r.status_code)

        r = requests.get(f"{task_url}{task_id}")
        self.assertEqual(task_id, json.loads(r.text)["id"])
        self.assertEqual("newTaskName", json.loads(r.text)["name"])
        self.assertEqual("newTag", json.loads(r.text)["tag"])
        self.assertEqual(None, json.loads(r.text)["attachments"])
        self.assertEqual(None, json.loads(r.text)["instructions"])

        r = requests.delete(f"{task_url}{task_id}")
        self.assertIsNotNone(r)
        self.assertEqual(204, r.status_code)
