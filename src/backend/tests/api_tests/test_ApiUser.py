import unittest
import requests, json
from src.backend.config import config


class ApiUserTest(unittest.TestCase):
    def test_createAndDeleteUser(self):
        """
        Test Case for creating and deleting the user.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/addUser"
        user_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/user/"
        user_dict = {
            "username": "tuser",
            "first_name": "test",
            "last_name": "user",
            "email": "test.user@mail.com",
            "password": "myPassword",
            "tag": "usertag"
        }

        # creating the user
        r = requests.post(create_url, json=user_dict)
        self.assertIsNotNone(r)
        self.assertIsInstance(int(r.text), int)
        self.assertEqual(200, r.status_code)
        user_id = r.text

        # checks after creation
        r = requests.get(f"{user_url}{user_id}")
        self.assertEqual(200, r.status_code)
        self.assertEqual("tuser", json.loads(r.text)["username"])
        self.assertEqual("test", json.loads(r.text)["first_name"])
        self.assertEqual("user", json.loads(r.text)["last_name"])
        self.assertEqual("test.user@mail.com", json.loads(r.text)["email"])
        self.assertEqual("myPassword", json.loads(r.text)["password"])
        self.assertEqual("usertag", json.loads(r.text)["tag"])

        # deleting the user after the test
        r = requests.delete(f"{user_url}{user_id}")
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)

    def test_createUpdateAndDeleteUser(self):
        """
        Test Case for creating, updating and then deleting the user again via API
        Covers post, get, put and delete for the api/user
        @return: No return
        """

        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/addUser"
        user_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/user/"
        user_dict = {
            "username": "tuser",
            "first_name": "test",
            "last_name": "user",
            "email": "test.user@mail.com",
            "password": "myPassword",
            "tag": "usertag"
        }

        # creating the user
        r = requests.post(create_url, json=user_dict)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        user_id = r.text

        # checks after creation
        r = requests.get(f"{user_url}{user_id}")
        self.assertEqual(200, r.status_code)
        self.assertEqual("tuser", json.loads(r.text)["username"])
        self.assertEqual("test", json.loads(r.text)["first_name"])
        self.assertEqual("user", json.loads(r.text)["last_name"])
        self.assertEqual("test.user@mail.com", json.loads(r.text)["email"])
        self.assertEqual("myPassword", json.loads(r.text)["password"])
        self.assertEqual("usertag", json.loads(r.text)["tag"])

        new_user_dict = {
            "username": "new",
            "first_name": "first",
            "last_name": "last",
            "email": "test.user@mail.com",
            "password": "myNewPassword",
            "tag": "newUserTag"
        }

        # updating the user
        r = requests.put(f"{user_url}{user_id}", json=new_user_dict, headers={'content-type': 'application/json'})
        self.assertEqual(200, r.status_code)

        # checking again
        r = requests.get(f"{user_url}{user_id}")
        self.assertEqual(200, r.status_code)
        self.assertEqual("new", json.loads(r.text)["username"])
        self.assertEqual("first", json.loads(r.text)["first_name"])
        self.assertEqual("last", json.loads(r.text)["last_name"])
        self.assertEqual("test.user@mail.com", json.loads(r.text)["email"])
        self.assertEqual("myNewPassword", json.loads(r.text)["password"])
        self.assertEqual("newUserTag", json.loads(r.text)["tag"])

        # deleting the user after the test
        r = requests.delete(f"{user_url}{user_id}")
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
