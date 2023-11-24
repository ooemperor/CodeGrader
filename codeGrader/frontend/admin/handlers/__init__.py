"""
Init File for the handlers of the admin WebServer.
@author: mkaiser
"""

from .Login import AdminUserLoginHandler
from .SessionAdmin import AdminSessionHandler, SessionAdmin
from .User import UserListHandler, UserHandler, AddUserHandler, DeleteUserHandler
from .Home import HomeHandler
from .AdminUser import AdminListHandler, AdminHandler, AddAdminHandler, DeleteAdminHandler
from .Profile import ProfileHandler, ProfileListHandler, AddProfileHandler, DeleteProfileHandler
from .Subject import SubjectHandler, SubjectListHandler, AddSubjectHandler, DeleteSubjectHandler
from .Task import TaskHandler, TaskListHandler, AddTaskHandler, DeleteTaskHandler
from .Exercise import ExerciseHandler, ExerciseListHandler, AddExerciseHandler, DeleteExerciseHandler

__all__ = ["AdminUserLoginHandler", "AdminSessionHandler", "SessionAdmin", "UserListHandler", "UserHandler",
           "HomeHandler", "AdminHandler", "AdminListHandler", "ProfileListHandler", "ProfileHandler",
           "SubjectListHandler", "SubjectHandler", "ExerciseListHandler", "ExerciseHandler", "TaskHandler",
           "TaskListHandler", "AddAdminHandler", "AddProfileHandler", "AddExerciseHandler", "AddTaskHandler",
           "AddSubjectHandler", "AddUserHandler", "DeleteUserHandler", "DeleteTaskHandler", "DeleteAdminHandler",
           "DeleteProfileHandler", "DeleteExerciseHandler", "DeleteUserHandler", "DeleteSubjectHandler"]
