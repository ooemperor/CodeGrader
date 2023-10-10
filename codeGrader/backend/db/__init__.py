"""
Init file for all the Database Models for the deployment
Imports all the classes in this directory
@author: mkaiser
"""
import sqlalchemy as sql

from codeGrader.backend.config import config


__all__ = ["User", "AdminUser", "Profile", "Task", "Base", "dbEngine", "Session", "Subject", "Exercise", "File"]

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


"""
Classes to do in first draft:
User ==> AdminUser
UserProfile_lnk
Profile

Lecture
Task
Exercise
Attachment

Submission
SubmissionResult
File

"""
