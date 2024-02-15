# CodeGrader - https://github.com/ooemperor/CodeGrader
# Copyright © 2023, 2024 Michael Kaiser <michael.kaiser@emplabs.ch>
#
# This file is part of CodeGrader.
#
# CodeGrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CodeGrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CodeGrader.  If not, see <http://www.gnu.org/licenses/>.

"""
Init File for the handlers of the admin WebServer.
@author: mkaiser
"""

from .Login import AdminUserLoginHandler
from .SessionAdmin import AdminSessionHandler, SessionAdmin
from .User import UserListHandler, UserHandler, AddUserHandler, DeleteUserHandler, AddUserListHandler
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
from .Membership import AddMembershipHandler, DeleteMembershipHandler
from .PasswordReset import PasswordResetHandler
from .Error import ErrorHandler

__all__ = ["AdminUserLoginHandler", "AdminSessionHandler", "SessionAdmin", "UserListHandler", "UserHandler",
           "HomeHandler", "AdminHandler", "AdminListHandler", "ProfileListHandler", "ProfileHandler",
           "SubjectListHandler", "SubjectHandler", "ExerciseListHandler", "ExerciseHandler", "TaskHandler",
           "TaskListHandler", "AddAdminHandler", "AddProfileHandler", "AddExerciseHandler", "AddTaskHandler",
           "AddSubjectHandler", "AddUserHandler", "DeleteUserHandler", "DeleteTaskHandler", "DeleteAdminHandler",
           "DeleteProfileHandler", "DeleteExerciseHandler", "DeleteUserHandler", "DeleteSubjectHandler",
           "AddTaskAttachmentHandler", "AddTaskInstructionHandler", "DeleteTaskAttachmentHandler",
           "DeleteTaskInstructionHandler", "TaskInstructionHandler", "TaskAttachmentHandler", "SubmissionFileHandler",
           "TestCaseInputFileHandler", "TestCaseOutputFileHandler", "AddTestCaseHandler", "DeleteTestCaseHandler",
           "AddMembershipHandler", "DeleteMembershipHandler", "PasswordResetHandler", "AddUserListHandler",
           "ErrorHandler"]
