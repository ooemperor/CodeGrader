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


class ApiFileTest(unittest.TestCase):

    def setUp(self):
        self.headers = dict()
        self.headers["Authorization"] = f"{api_config.apiAuthentication} {api_config.apiToken}"

    def test_createAndDeleteExercise(self):
        """
        Test Case for creating and deleting a file in the database
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/file/upload"
        file_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/file/"

        test_file = open("./backend/api_tests/AFileForTesting.txt", 'rb')

        files = {"AFileForTesting.txt": test_file}
        r = requests.post(create_url, files=files, headers=self.headers)
        test_file.close()
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        file_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{file_url}{file_id}", headers=self.headers)
        self.assertEqual(200, r.status_code)

        r = requests.delete(f"{file_url}{file_id}", headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(204, r.status_code)
