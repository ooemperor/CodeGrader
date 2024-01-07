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
from .TaskAttachment import AddTaskAttachmentHandler, DeleteTaskAttachmentHandler, TaskAttachmentHandler
from .TaskInstruction import AddTaskInstructionHandler, DeleteTaskInstructionHandler, TaskInstructionHandler
from .Submission import SubmissionFileHandler
from .TestCase import TestCaseInputFileHandler, TestCaseOutputFileHandler, AddTestCaseHandler, DeleteTestCaseHandler

__all__ = ["AdminUserLoginHandler", "AdminSessionHandler", "SessionAdmin", "UserListHandler", "UserHandler",
           "HomeHandler", "AdminHandler", "AdminListHandler", "ProfileListHandler", "ProfileHandler",
           "SubjectListHandler", "SubjectHandler", "ExerciseListHandler", "ExerciseHandler", "TaskHandler",
           "TaskListHandler", "AddAdminHandler", "AddProfileHandler", "AddExerciseHandler", "AddTaskHandler",
           "AddSubjectHandler", "AddUserHandler", "DeleteUserHandler", "DeleteTaskHandler", "DeleteAdminHandler",
           "DeleteProfileHandler", "DeleteExerciseHandler", "DeleteUserHandler", "DeleteSubjectHandler",
           "AddTaskAttachmentHandler", "AddTaskInstructionHandler", "DeleteTaskAttachmentHandler",
           "DeleteTaskInstructionHandler", "TaskInstructionHandler", "TaskAttachmentHandler", "SubmissionFileHandler",
           "TestCaseInputFileHandler", "TestCaseOutputFileHandler", "AddTestCaseHandler", "DeleteTestCaseHandler"]
