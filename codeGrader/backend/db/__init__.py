"""
Init file for all the Database Models for the deployment
Imports all the classes in this directory
@author: mkaiser
"""
import sqlalchemy as sql

from codeGrader.backend.config import (config)

__all__ = ["User", "AdminUser", "Profile", "Task", "Base", "dbEngine", "Session", "Subject", "Exercise", "File",
           "Attachment", "Instruction", "test_DB", "delete_DB", "create_DB", "Submission"]

# creation of the db engine
dbEngine = sql.create_engine(config.dbConnectionString)

# import of all the datamodels.
# import cannot not be on top of file because of the dbEngine
from .Profile import Profile
from .User import User, AdminUser
from .Subject import Subject
from .Membership import Membership
from .Exercise import Exercise
from .Task import Task
from .Base import Base
from .Session import Session
from .File import File
from .Attachments import Attachment, Instruction
from .Submission import Submission
from .DBScripts import test_DB, create_DB, delete_DB

"""
Classes to do in first draft:
Attachment

Submission
SubmissionResult
File

"""
