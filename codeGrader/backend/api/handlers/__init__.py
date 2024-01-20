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
from .Score import ScoreHandler
from .PasswordReset import AdminUserPasswordResetHandler, UserPasswordResetHandler
from .Membership import MembershipHandler

__all__ = ["BaseHandler", "UserHandler", "AdminUserHandler", "ProfileHandler", "SubjectHandler", "TaskHandler",
           "ExerciseHandler", "FileHandler", "SubmissionHandler", "authentication", "AuthorizationFail",
           "TestCaseHandler", "AdminUserLoginHandler", "AdminTypeHandler", "UserLoginHandler", "AttachmentHandler",
           "InstructionHandler", "ScoreHandler", "AdminUserPasswordResetHandler", "UserPasswordResetHandler",
           "MembershipHandler"]
