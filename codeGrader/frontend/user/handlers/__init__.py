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
Init File for the Handler Classes of the User Frontend.
"""

from .Base import BaseHandler
from .SessionUser import UserSessionHandler, SessionUser
from .Login import UserLoginHandler
from .Home import HomeHandler
from .Exercise import ExerciseListHandler, ExerciseHandler
from .Task import TaskHandler, TaskListHandler
from .TaskAttachment import TaskAttachmentHandler
from .TaskInstruction import TaskInstructionHandler
from .Submission import AddSubmissionHandler
from .Settings import SettingsHandler
from .PasswordReset import PasswordResetHandler

__all__ = ["BaseHandler", "UserSessionHandler", "SessionUser", "UserLoginHandler", "HomeHandler", "ExerciseListHandler",
           "ExerciseHandler", "TaskHandler", "TaskListHandler", "TaskAttachmentHandler", "TaskInstructionHandler",
           "AddSubmissionHandler", "SettingsHandler", "PasswordResetHandler"]
