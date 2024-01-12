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


class ApiProfileTest(unittest.TestCase):

    def setUp(self):
        self.headers = dict()
        self.headers["Authorization"] = f"{api_config.apiAuthentication} {api_config.apiToken}"

    def test_createAndDeleteProfile(self):
        """
        Test Case for creating and deleting the Profile.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/profile/add"
        profile_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/profile/"

        profile_dict = {
            "name": "testProfile",
            "tag": "profiletag"
        }
        r = requests.post(create_url, json=profile_dict, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        profile_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{profile_url}{profile_id}", headers=self.headers)
        self.assertEqual(200, r.status_code)
        self.assertEqual("testProfile", json.loads(r.text)["name"])
        self.assertEqual("profiletag", json.loads(r.text)["tag"])

        r = requests.delete(f"{profile_url}{profile_id}", headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(204, r.status_code)

    def test_createUpdateAndDeleteProfile(self):
        """
        Test Case for creating and deleting the Profile.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/profile/add"
        profile_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/profile/"

        profile_dict = {
            "name": "testProfile",
            "tag": "profiletag"
        }

        profile_dict_2 = {
            "name": "newProfileName",
            "tag": "newTag"
        }
        r = requests.post(create_url, json=profile_dict, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        profile_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{profile_url}{profile_id}", headers=self.headers)
        self.assertEqual(200, r.status_code)
        self.assertEqual(profile_id, json.loads(r.text)["id"])
        self.assertEqual("testProfile", json.loads(r.text)["name"])
        self.assertEqual("profiletag", json.loads(r.text)["tag"])

        r = requests.put(f"{profile_url}{profile_id}", json=profile_dict_2, headers={'content-type': 'application/json',
                                                                                     'Authorization': f"{api_config.apiAuthentication} {api_config.apiToken}"})
        self.assertEqual(200, r.status_code)

        r = requests.get(f"{profile_url}{profile_id}", headers=self.headers)
        self.assertEqual(profile_id, json.loads(r.text)["id"])
        self.assertEqual("newProfileName", json.loads(r.text)["name"])
        self.assertEqual("newTag", json.loads(r.text)["tag"])

        r = requests.delete(f"{profile_url}{profile_id}", headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(204, r.status_code)

    def test_GETProfilesEndpoint(self):
        """
        Test Case for the testing if the /profiles endpoint is working
        @return: No return
        """
        url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/profiles"

        r = requests.get(url, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        self.assertIsNotNone(json.loads(r.text)["profile"])
