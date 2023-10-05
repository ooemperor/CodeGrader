import unittest
import requests, json
from src.backend.config import config


class ApiProfileTest(unittest.TestCase):
    def test_createAndDeleteProfile(self):
        """
        Test Case for creating and deleting the Profile.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/addProfile"
        profile_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/profile/"

        profile_dict = {
            "name": "testProfile",
            "tag": "profiletag"
        }
        r = requests.post(create_url, json=profile_dict)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        profile_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{profile_url}{profile_id}")
        self.assertEqual(200, r.status_code)
        self.assertEqual("testProfile", json.loads(r.text)["name"])
        self.assertEqual("profiletag", json.loads(r.text)["tag"])

        r = requests.delete(f"{profile_url}{profile_id}")
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)

    def test_createUpdateAndDeleteProfile(self):
        """
        Test Case for creating and deleting the Profile.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/addProfile"
        profile_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/profile/"

        profile_dict = {
            "name": "testProfile",
            "tag": "profiletag"
        }

        profile_dict_2 = {
            "name": "newProfileName",
            "tag": "newTag"
        }
        r = requests.post(create_url, json=profile_dict)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        profile_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{profile_url}{profile_id}")
        self.assertEqual(200, r.status_code)
        self.assertEqual(profile_id, json.loads(r.text)["id"])
        self.assertEqual("testProfile", json.loads(r.text)["name"])
        self.assertEqual("profiletag", json.loads(r.text)["tag"])

        r = requests.put(f"{profile_url}{profile_id}", json=profile_dict_2, headers={'content-type': 'application/json'})
        self.assertEqual(200, r.status_code)

        r = requests.get(f"{profile_url}{profile_id}")
        self.assertEqual(profile_id, json.loads(r.text)["id"])
        self.assertEqual("newProfileName", json.loads(r.text)["name"])
        self.assertEqual("newTag", json.loads(r.text)["tag"])

        r = requests.delete(f"{profile_url}{profile_id}")
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
