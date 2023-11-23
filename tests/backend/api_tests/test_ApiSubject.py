import unittest
import requests, json
from codeGrader.backend.config import config


class ApiSubjectTest(unittest.TestCase):
    def test_createAndDeleteSubject(self):
        """
        Test Case for creating and deleting the Task.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/subject/add"
        subject_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/subject/"

        subject_dict = {
            "name": "testSubject",
            "tag": "subjecttag"
        }
        r = requests.post(create_url, json=subject_dict)
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        subject_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{subject_url}{subject_id}")
        self.assertEqual(200, r.status_code)
        self.assertEqual("testSubject", json.loads(r.text)["name"])
        self.assertEqual("subjecttag", json.loads(r.text)["tag"])

        r = requests.delete(f"{subject_url}{subject_id}")
        self.assertIsNotNone(r)
        self.assertEqual(204, r.status_code)

    def test_createUpdateAndDeleteSubject(self):
        """
        Test Case for creating and deleting the Task.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/exercise/add"
        subject_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/exercise/"

        subject_dict = {
            "name": "testSubject",
            "tag": "subjecttag"
        }

        subject_dict_2 = {
            "name": "newSubjectName",
            "tag": "newTag"
        }
        r = requests.post(create_url, json=subject_dict)
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        subject_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{subject_url}{subject_id}")
        self.assertEqual(200, r.status_code)
        self.assertEqual(subject_id, json.loads(r.text)["id"])
        self.assertEqual("testSubject", json.loads(r.text)["name"])
        self.assertEqual("subjecttag", json.loads(r.text)["tag"])

        r = requests.put(f"{subject_url}{subject_id}", json=subject_dict_2, headers={'content-type': 'application/json'})
        self.assertEqual(200, r.status_code)

        r = requests.get(f"{subject_url}{subject_id}")
        self.assertEqual(subject_id, json.loads(r.text)["id"])
        self.assertEqual("newSubjectName", json.loads(r.text)["name"])
        self.assertEqual("newTag", json.loads(r.text)["tag"])

        r = requests.delete(f"{subject_url}{subject_id}")
        self.assertIsNotNone(r)
        self.assertEqual(204, r.status_code)
