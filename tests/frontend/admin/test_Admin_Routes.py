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

        self.url = f"http://{config.tests_frontendHost}:{config.tests_adminPort}/"
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

    def test_GET_admins(self):
        """
        Test Case for the /admins route
        @return: No return
        """
        route = "admins"
        r = requests.get(self.url+route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertFalse("input input_login" in r.text)

    def test_GET_admin_add(self):
        """
        Test Case for the /admin/add route
        @return: No return
        """
        route = "admin/add"
        r = requests.get(self.url+route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertFalse("input input_login" in r.text)

    def test_GET_users(self):
        """
        Test Case for the /users route
        @return: No return
        """
        route = "users"
        r = requests.get(self.url+route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertFalse("input input_login" in r.text)

    def test_GET_user_add(self):
        """
        Test Case for the /user/add route
        @return: No return
        """
        route = "user/add"
        r = requests.get(self.url+route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertFalse("input input_login" in r.text)

    def test_GET_profiles(self):
        """
        Test Case for the /profiles route
        @return: No return
        """
        route = "profiles"
        r = requests.get(self.url+route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertFalse("input input_login" in r.text)

    def test_GET_profile_add(self):
        """
        Test Case for the /profile/add route
        @return: No return
        """
        route = "profile/add"
        r = requests.get(self.url+route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertFalse("input input_login" in r.text)

    def test_GET_subjects(self):
        """
        Test Case for the /subjects route
        @return: No return
        """
        route = "subjects"
        r = requests.get(self.url+route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertFalse("input input_login" in r.text)

    def test_GET_subject_add(self):
        """
        Test Case for the /subject/add route
        @return: No return
        """
        route = "subject/add"
        r = requests.get(self.url+route, cookies=self.cookies)
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

    def test_GET_exercise_add(self):
        """
        Test Case for the /exercise/add route
        @return: No return
        """
        route = "exercise/add"
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

    def test_GET_task_add(self):
        """
        Test Case for the /task/add route
        @return: No return
        """
        route = "task/add"
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
