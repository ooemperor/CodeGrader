"""
Init file for all the API Handler
Imports all the classes and functions in this directory
@author: mkaiser
"""
from .Base import BaseHandler
from .User import UserHandler, AdminUserHandler
from .Profile import ProfileHandler
from .Subject import SubjectHandler
from .Task import TaskHandler
from .Exercise import ExerciseHandler
from .File import FileHandler
from .Submission import SubmissionHandler
from .Exceptions import AuthorizationFail
from .Authentication import authentication
from .TestCase import TestCaseHandler
from .LoginHandler import LoginHandler

__all__ = ["BaseHandler", "UserHandler", "AdminUserHandler", "ProfileHandler", "SubjectHandler", "TaskHandler",
           "ExerciseHandler", "FileHandler", "SubmissionHandler", "authentication", "AuthorizationFail",
           "TestCaseHandler", "LoginHandler"]
