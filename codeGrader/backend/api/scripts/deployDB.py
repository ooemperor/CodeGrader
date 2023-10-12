"""
Completely redeploying the Database.
@author: mkaiser
@see: codeGrader.backend.db
"""

from codeGrader.backend.db import test_DB, delete_DB, create_DB

if test_DB() is True:
    delete_DB()
    create_DB()
