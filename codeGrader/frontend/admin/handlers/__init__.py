"""
Init File for the handlers of the admin WebServer.
@author: mkaiser
"""

from .Login import AdminUserLoginHandler
from .SessionAdminUser import AdminUserSessionHandler, SessionAdminUser
from .User import UserListHandler, UserHandler, AddUserHandler
from .Home import HomeHandler
from .AdminUser import AdminUserListHandler, AdminUserHandler, AddAdminUserHandler
from .Profile import ProfileHandler, ProfileListHandler, AddProfileHandler
from .Subject import SubjectHandler, SubjectListHandler, AddSubjectHandler
from .Task import TaskHandler, TaskListHandler, AddTaskHandler
from .Exercise import ExerciseHandler, ExerciseListHandler, AddExerciseHandler

__all__ = ["AdminUserLoginHandler", "AdminUserSessionHandler", "SessionAdminUser", "UserListHandler", "UserHandler",
           "HomeHandler", "AdminUserHandler", "AdminUserListHandler", "ProfileListHandler", "ProfileHandler",
           "SubjectListHandler", "SubjectHandler", "ExerciseListHandler", "ExerciseHandler", "TaskHandler",
           "TaskListHandler", "AddAdminUserHandler", "AddProfileHandler", "AddExerciseHandler", "AddTaskHandler",
           "AddSubjectHandler", "AddUserHandler"]
