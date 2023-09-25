"""
Dropping the database according to the datamodel
@author: mkaiser
@see: src.backend.db
"""

from src.backend.db.DBScripts import test_DB, delete_DB
if test_DB() is True:
    delete_DB()
