"""
Completely redeploying the Database.
@author: mkaiser
@see: src.backend.db
"""

from ..db.DBScripts import test_DB, delete_DB, create_DB

if test_DB() is True:
    delete_DB()
    create_DB()
