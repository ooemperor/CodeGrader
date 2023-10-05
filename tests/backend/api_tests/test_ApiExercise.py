import unittest
import requests, json
from src.backend.config import config


class ApiExerciseTest(unittest.TestCase):
    def test_createAndDeleteExercise(self):
        """
        Test Case for creating and deleting the Exercise.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/addExercise"
        exercise_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/exercise/"

        exercise_dict = {
            "name": "testExercise",
            "tag": "exercisetag"
        }
        r = requests.post(create_url, json=exercise_dict)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        exercise_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{exercise_url}{exercise_id}")
        self.assertEqual(200, r.status_code)
        self.assertEqual("testExercise", json.loads(r.text)["name"])
        self.assertEqual("exercisetag", json.loads(r.text)["tag"])

        r = requests.delete(f"{exercise_url}{exercise_id}")
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)

    def test_createUpdateAndDeleteExercise(self):
        """
        Test Case for creating and deleting the Exercise.
        Covers post, get and delete for the api/user
        @return: No return
        """
        create_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/addExercise"
        exercise_url = f"http://{config.tests_ApiHost}:{config.tests_ApiPort}/exercise/"

        exercise_dict = {
            "name": "testExercise",
            "tag": "exerciseTag"
        }

        exercise_dict_2 = {
            "name": "newExerciseName",
            "tag": "newTag"
        }
        r = requests.post(create_url, json=exercise_dict)
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
        exercise_id = json.loads(r.text)["response"]["id"]

        r = requests.get(f"{exercise_url}{exercise_id}")
        self.assertEqual(200, r.status_code)
        self.assertEqual(exercise_id, json.loads(r.text)["id"])
        self.assertEqual("testExercise", json.loads(r.text)["name"])
        self.assertEqual("exerciseTag", json.loads(r.text)["tag"])

        r = requests.put(f"{exercise_url}{exercise_id}", json=exercise_dict_2, headers={'content-type': 'application/json'})
        self.assertEqual(200, r.status_code)

        r = requests.get(f"{exercise_url}{exercise_id}")
        self.assertEqual(exercise_id, json.loads(r.text)["id"])
        self.assertEqual("newExerciseName", json.loads(r.text)["name"])
        self.assertEqual("newTag", json.loads(r.text)["tag"])

        r = requests.delete(f"{exercise_url}{exercise_id}")
        self.assertIsNotNone(r)
        self.assertEqual(200, r.status_code)
