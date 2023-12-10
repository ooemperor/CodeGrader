import unittest
import requests, json
from codeGrader.backend.config import config


class ApiFileTest(unittest.TestCase):
    def test_createAndDeleteExercise(self):
        """
        Test Case for creating and deleting a file in the database
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/file/upload"
        file_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/file/"

        test_file = open("./backend/api_tests/AFileForTesting.txt", 'rb')

        files = {"AFileForTesting.txt": test_file}
        r = requests.post(create_url, files=files)
        test_file.close()
        self.assertIsNotNone(r)
        self.assertEqual(201, r.status_code)
        file_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{file_url}{file_id}")
        self.assertEqual(200, r.status_code)

        r = requests.delete(f"{file_url}{file_id}")
        self.assertIsNotNone(r)
        self.assertEqual(204, r.status_code)
