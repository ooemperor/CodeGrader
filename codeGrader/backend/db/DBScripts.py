# CodeGrader - https://github.com/ooemperor/CodeGrader
# Copyright © 2023, 2024 Michael Kaiser <michael.kaiser@emplabs.ch>
#
# This file is part of CodeGrader.
#
# CodeGrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CodeGrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CodeGrader.  If not, see <http://www.gnu.org/licenses/>.

"""
File for mulitple helper functions, that are associated with the Database
@author: mkaiser
"""
from codeGrader.backend.config import config
from .AdminType import AdminType
from .Session import Session
import psycopg2

from . import Base, dbEngine


def __executeSqlOnDB(sqlStatement: str) -> bool:
    """
    Executes a SQL Statement on the database
    @param sqlStatement: the Statement that shall be executed.
    @return: The output of the query
    @rtype:
    """
    conn = psycopg2.connect(user=config.DBUser, password=config.DBPassword, host=config.DBHost, port=config.DBPort, dbname=config.DBName)
    cur = conn.cursor()
    cur.execute(sqlStatement)
    conn.commit()
    cur.close()
    conn.close()
    return True


def test_DB() -> bool:
    """
    Tests the DB Connection
    @return: True for succesful Database connection, else false.
    """
    __executeSqlOnDB('SELECT VERSION();')
    return True


def create_DB() -> bool:
    """
    Creates the database based on the metadata.
    @return: True if success else throws an error.
    """
    Base.metadata.create_all(dbEngine)
    print("The following tables have been deployed: ")
    for table in Base.metadata.tables.keys():
        print("\t" + table)
    print("Setting up the default table values:")
    init_DB_Data()
    print("Data has bee inserted")

    return True


def delete_DB() -> bool:
    """
    Deleting all the Data and the schema public of the database and then recreating the schema public
    @return: True if successful, else throws error
    """
    __executeSqlOnDB("DROP SCHEMA public CASCADE;")
    __executeSqlOnDB("CREATE SCHEMA public;")
    print("Schema has been deleted and recreated!")
    return True


def init_DB_Data() -> bool:
    """
    Initialize the basic values in the database that need to be defined from the start on.
    @return: True on success else raises an error
    """
    # the definition of the admin types
    admin_types = [
        {"name": "Super Admin", "description": "The Super Admin that has every right on every object"},
        {"name": "Profile Admin", "description": "The Profile Admin only has rights on its Profile"},
        {"name": "Read Only Full Admin", "description": "The Read Only Full Admin can only read but cannot make changes to any object"},
        {"name": "Read Only Profile Admin", "description": "The Read Only Profile Admin can only read on the profiles objects but cannot make changes to any object"}
     ]

    session = Session()
    for admin_type in admin_types:
        at = AdminType(**admin_type)
        session.create(at)

    return True
