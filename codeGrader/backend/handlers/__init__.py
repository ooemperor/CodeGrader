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

__all__ = ["BaseHandler", "UserHandler", "AdminUserHandler", "ProfileHandler", "SubjectHandler", "TaskHandler",
           "ExerciseHandler"]
