"""
Init file for all the Database Models for the deployment
Imports all the classes in this directory
@author: mkaiser
"""
import sqlalchemy as sql
from src.backend.config import Config

# TODO: Import all the Databasemodels after writing
config = Config.Config()
dbEngine = sql.create_engine(config.dbConnectionString)

from .User import User
from .Task import Task
from .Base import Base


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