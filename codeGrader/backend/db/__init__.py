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
Init file for all the Database Models for the deployment
Imports all the classes in this directory
@author: mkaiser
"""
import sqlalchemy as sql

from codeGrader.backend.config import (config)

__all__ = ["User", "AdminUser", "Profile", "Task", "Base", "dbEngine", "Session", "Subject", "Exercise", "File",
           "Attachment", "Instruction", "test_DB", "delete_DB", "create_DB", "Submission", "APIToken",
           "ExecutionResult", "EvaluationResult", "TestCase", "AdminType"]

# creation of the db engine
dbEngine = sql.create_engine(config.dbConnectionString)

# import of all the datamodels.
# import cannot not be on top of file because of the dbEngine
from .Admin import AdminUser
from .AdminType import AdminType
from .Profile import Profile
from .User import User
from .Subject import Subject
from .Membership import Membership
from .Exercise import Exercise
from .Task import Task
from .Base import Base
from .Session import Session
from .File import File
from .Attachments import Attachment, Instruction
from .Submission import Submission
from .Authentication import APIToken
from .DBScripts import test_DB, create_DB, delete_DB
from .ExecutionResult import ExecutionResult
from .EvaluationResult import EvaluationResult
from .TestCase import TestCase

"""
Classes to do in first draft:
Attachment

Submission
SubmissionResult
File

"""
