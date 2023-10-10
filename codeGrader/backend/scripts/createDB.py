"""
Creating the database according to the datamodel
@author: mkaiser
@see: codeGrader.backend.db
"""

from codeGrader.backend.db.DBScripts import test_DB, create_DB

if test_DB() is True:
    create_DB()
