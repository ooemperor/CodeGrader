"""
Init file for all api_tests for the tests root folder
Imports all the classes in this directory
@author: mkaiser
"""

from . import test_ApiUser, test_ApiExercise, test_ApiTask, test_ApiProfile, test_ApiSubject

__all__ = [test_ApiUser, test_ApiExercise, test_ApiTask, test_ApiProfile, test_ApiSubject]
