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


class ApiMembershipTest(unittest.TestCase):

    def setUp(self):
        self.headers = dict()
        self.headers["Authorization"] = f"{api_config.apiAuthentication} {api_config.apiToken}"

    def test_GETMembershipsEndpoint(self):
        """
        Test Case for the testing if the /memberships endpoint is working
        @return: No return
        """
        url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/memberships"

        r = requests.get(url, headers=self.headers)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
