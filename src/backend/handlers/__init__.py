"""
Init file for all the API Handler
Imports all the classes and functions in this directory
@author: mkaiser
"""
from src.backend.handlers.Base import BaseHandler
from src.backend.handlers.User import UserHandler, AdminUserHandler
from src.backend.handlers.Profile import ProfileHandler
from src.backend.handlers.Subject import SubjectHandler
from src.backend.handlers.Task import TaskHandler
from src.backend.handlers.Execercise import ExerciseHandler

__all__ = ["BaseHandler", "UserHandler", "AdminUserHandler", "ProfileHandler", "SubjectHandler", "TaskHandler",
           "ExerciseHandler"]
