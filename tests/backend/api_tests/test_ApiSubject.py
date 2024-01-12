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


class ApiSubjectTest(unittest.TestCase):

    def setUp(self):
        self.headers = dict()
        self.headers["Authorization"] = f"{api_config.apiAuthentication} {api_config.apiToken}"

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
        r = requests.post(create_url, json=subject_dict, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        subject_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{subject_url}{subject_id}", headers=self.headers)
        self.assertEqual(200, r.status_code)
        self.assertEqual("testSubject", json.loads(r.text)["name"])
        self.assertEqual("subjecttag", json.loads(r.text)["tag"])

        r = requests.delete(f"{subject_url}{subject_id}", headers=self.headers)
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
        r = requests.post(create_url, json=subject_dict, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        subject_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{subject_url}{subject_id}", headers=self.headers)
        self.assertEqual(200, r.status_code)
        self.assertEqual(subject_id, json.loads(r.text)["id"])
        self.assertEqual("testSubject", json.loads(r.text)["name"])
        self.assertEqual("subjecttag", json.loads(r.text)["tag"])

        r = requests.put(f"{subject_url}{subject_id}", json=subject_dict_2, headers={'content-type': 'application/json',
                                                                                     'Authorization': f"{api_config.apiAuthentication} {api_config.apiToken}"})
        self.assertEqual(200, r.status_code)

        r = requests.get(f"{subject_url}{subject_id}", headers=self.headers)
        self.assertEqual(subject_id, json.loads(r.text)["id"])
        self.assertEqual("newSubjectName", json.loads(r.text)["name"])
        self.assertEqual("newTag", json.loads(r.text)["tag"])

        r = requests.delete(f"{subject_url}{subject_id}", headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(204, r.status_code)

    def test_GETSubjectsEndpoint(self):
        """
        Test Case for the testing if the /subjects endpoint is working
        @return: No return
        """
        url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/subjects"

        r = requests.get(url, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(json.loads(r.text)["subject"])
