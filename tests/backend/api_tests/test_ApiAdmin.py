import unittest
import requests, json
from codeGrader.backend.config import config
from codeGrader.frontend.config import config as api_config


class ApiAdminUserTest(unittest.TestCase):

    def setUp(self):
        self.headers = dict()
        self.headers["Authorization"] = f"{api_config.apiAuthentication} {api_config.apiToken}"

    def test_createAndDeleteAdminUser(self):
        """
        Test Case for creating and deleting the AdminUser.
        Covers post, get and delete for the api/user
        @return: No return
        """
        headers = dict()
        headers["Authorization"] = f"{api_config.apiAuthentication} {api_config.apiToken}"
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/admin/add"
        adminUser_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/admin/"
        adminUser_dict = {
            "username": "admin_test",
            "first_name": "admin",
            "last_name": "user",
            "email": "test.user@mail.com",
            "password": "myPassword",
            "tag": "usertag",
            "admin_type": 1
        }

        # creating the user
        r = requests.post(create_url, json=adminUser_dict, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        adminUser_id = json.loads(r.text)["response"]["id"]

        # checks after creation
        r = requests.get(f"{adminUser_url}{adminUser_id}", headers=self.headers)
        self.assertEqual(200, r.status_code)
        self.assertEqual("admin_test", json.loads(r.text)["username"])
        self.assertEqual("admin", json.loads(r.text)["first_name"])
        self.assertEqual("user", json.loads(r.text)["last_name"])
        self.assertEqual("test.user@mail.com", json.loads(r.text)["email"])
        self.assertEqual("usertag", json.loads(r.text)["tag"])

        # deleting the user after the test
        r = requests.delete(f"{adminUser_url}{adminUser_id}", headers=self.headers)
        self.assertEqual(204, r.status_code)
        self.assertIsNotNone(r)

    def test_createUpdateAndDeleteAdminUser(self):
        """
        Test Case for creating, updating and then deleting the user again via API
        Covers post, get, put and delete for the api/user
        @return: No return
        """

        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/admin/add"
        adminUser_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/admin/"
        user_dict = {
            "username": "admin_test",
            "first_name": "admin",
            "last_name": "user",
            "email": "test.user@mail.com",
            "password": "myPassword",
            "tag": "usertag",
            "admin_type": 1
        }

        # creating the user
        r = requests.post(create_url, json=user_dict, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        adminUser_id = json.loads(r.text)["response"]["id"]

        # checks after creation
        r = requests.get(f"{adminUser_url}{adminUser_id}", headers=self.headers)
        self.assertEqual(200, r.status_code)
        self.assertEqual("admin_test", json.loads(r.text)["username"])
        self.assertEqual("admin", json.loads(r.text)["first_name"])
        self.assertEqual("user", json.loads(r.text)["last_name"])
        self.assertEqual("test.user@mail.com", json.loads(r.text)["email"])
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
        r = requests.put(f"{adminUser_url}{adminUser_id}", json=new_user_dict, headers={'content-type': 'application/json', 'Authorization': f"{api_config.apiAuthentication} {api_config.apiToken}"})
        self.assertEqual(200, r.status_code)

        # checking again
        r = requests.get(f"{adminUser_url}{adminUser_id}", headers=self.headers)
        self.assertEqual(200, r.status_code)
        self.assertEqual("new", json.loads(r.text)["username"])
        self.assertEqual("first", json.loads(r.text)["first_name"])
        self.assertEqual("last", json.loads(r.text)["last_name"])
        self.assertEqual("test.user@mail.com", json.loads(r.text)["email"])
        self.assertEqual("newUserTag", json.loads(r.text)["tag"])

        # deleting the user after the test
        r = requests.delete(f"{adminUser_url}{adminUser_id}", headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(204, r.status_code)

    def test_GETAdminsEndpoint(self):
        """
        Test Case for the testing if the /admins endpoint is working
        @return: No return
        """
        url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/admins"

        r = requests.get(url, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(json.loads(r.text)["adminuser"])

