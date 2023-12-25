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
