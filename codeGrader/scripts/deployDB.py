"""
Completely redeploying the Database.
@author: mkaiser
@see: codeGrader.backend.db
"""
import sys
from codeGrader.backend.db import test_DB, delete_DB, create_DB

def main():
    if test_DB() is True:
        delete_DB()
        create_DB()


if __name__ == '__main__':
    sys.exit(main())
