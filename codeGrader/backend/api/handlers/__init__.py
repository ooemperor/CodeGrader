"""
Init file for all the API Handler
Imports all the classes and functions in this directory
@author: mkaiser
"""
from .Base import BaseHandler
from .User import UserHandler
from .Admin import AdminUserHandler
from .AdminType import AdminTypeHandler
from .Profile import ProfileHandler
from .Subject import SubjectHandler
from .Task import TaskHandler
from .Attachment import AttachmentHandler
from .Instruction import InstructionHandler
from .Exercise import ExerciseHandler
from .File import FileHandler
from .Submission import SubmissionHandler
from .Exceptions import AuthorizationFail
from .Authentication import authentication
from .TestCase import TestCaseHandler
from .LoginHandler import AdminUserLoginHandler, UserLoginHandler

__all__ = ["BaseHandler", "UserHandler", "AdminUserHandler", "ProfileHandler", "SubjectHandler", "TaskHandler",
           "ExerciseHandler", "FileHandler", "SubmissionHandler", "authentication", "AuthorizationFail",
           "TestCaseHandler", "AdminUserLoginHandler", "AdminTypeHandler", "UserLoginHandler", "AttachmentHandler",
           "InstructionHandler"]
