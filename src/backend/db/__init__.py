"""
Init file for all the Database Models for the deployment
Imports all the classes in this directory
@author: mkaiser
"""
import sqlalchemy as sql

from src.backend.config import config


__all__ = ["User", "AdminUser", "Profile", "Task", "Base", "dbEngine"]

# TODO: Import all the Databasemodels after writing
dbEngine = sql.create_engine(config.dbConnectionString)

from src.backend.db.Profile import Profile
from src.backend.db.User import User, AdminUser
from src.backend.db.Subject import Subject
from src.backend.db.Membership import Membership
from src.backend.db.Exercise import Exercise
from src.backend.db.Task import Task
from src.backend.db.Base import Base




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
