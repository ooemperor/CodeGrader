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

        self.url = f"http://{config.tests_frontendHost}:{config.tests_userPort}/"
        login_data = {"username": self.username, "password": self.password}

        r = requests.post(self.url + "login", data=login_data)
        self.cookies = r.request._cookies

    def test_GET_static_png_Ube(self):
        """
        Test Case for checking if the static file routes are working for ube.png picture
        @return:
        """
        route = "static/img/ube.png"
        r = requests.get(self.url + route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)

    def test_GET_static_png_PHBern(self):
        """
        Test Case for checking if the static file routes are working for phbern.png picture
        @return:
        """
        route = "static/img/phbern.png"
        r = requests.get(self.url + route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)

    def test_GET_static_png_Belearn(self):
        """
        Test Case for checking if the static file routes are working for belearn.png picture
        @return:
        """
        route = "static/img/belearn.png"
        r = requests.get(self.url + route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)

    def test_GET_static_css_boostrap(self):
        """
        Test Case for checking if the static file routes are working for css boostrap picture
        @return:
        """
        route = "static/css/bootstrap.min.css"
        r = requests.get(self.url + route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)

    def test_GET_static_css_boostrap_icons(self):
        """
        Test Case for checking if the static file routes are working for css boostrap icons picture
        @return:
        """
        route = "static/css/bootstrap-icons.css"
        r = requests.get(self.url + route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)

    def test_GET_static_js_boostrap(self):
        """
        Test Case for checking if the static file routes are working for js boostrap picture
        @return:
        """
        route = "static/js/bootstrap.bundle.min.js"
        r = requests.get(self.url + route, cookies=self.cookies)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)


