"""
Dropping the database according to the datamodel
@author: mkaiser
@see: codeGrader.backend.db
"""

from codeGrader.backend.db import (test_DB, delete_DB)

if test_DB() is True:
    delete_DB()
