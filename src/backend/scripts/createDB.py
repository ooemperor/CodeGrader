"""
Creating the database according to the datamodel
@author: mkaiser
@see: src.backend.db
"""

from src.backend.db.DBScripts import test_DB, create_DB
if test_DB() is True:
    create_DB()
