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
