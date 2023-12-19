import unittest
import requests, json
from codeGrader.backend.config import config


class RouteTest(unittest.TestCase):

    def setUp(self):
        f = open("./frontend/admin/login.sec.json", 'rb')
        content = f.read()
        f.close()

        data = json.loads(content)
        self.username = data["username"]
        self.password = data["password"]

        self.url = f"http://{config.tests_frontendHost}:{config.tests_userPort}/"
        login_data = {"username": self.username, "password": self.password}

        r = requests.post(self.url + "login", data=login_data)
        self.cookies = r.request._cookies

    def test_GET_home(self):
        """
        Test Case for the /home route
        @return: No return
        """

        r = requests.get(self.url, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertFalse("input input_login" in r.text)

    def test_GET_exercises(self):
        """
        Test Case for the /exercises route
        @return: No return
        """
        route = "exercises"
        r = requests.get(self.url+route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertFalse("input input_login" in r.text)

    def test_GET_tasks(self):
        """
        Test Case for the /tasks route
        @return: No return
        """
        route = "tasks"
        r = requests.get(self.url+route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertFalse("input input_login" in r.text)

    def test_GET_logout(self):
        """
        Test Case for the /task/add route
        @return: No return
        """
        route = "logout"
        r = requests.get(self.url + route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertTrue("btn_login" in r.text)
