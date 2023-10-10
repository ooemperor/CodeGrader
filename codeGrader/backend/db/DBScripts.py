"""
File for mulitple helper functions, that are associated with the Database
@author: mkaiser
"""
from codeGrader.backend.config import config
import psycopg2

from codeGrader.backend.db import Base, dbEngine


def __executeSqlOnDB(sqlStatement):
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


def test_DB():
    """
    Tests the DB Connection
    @return: True for succesful Database connection, else false.
    """
    __executeSqlOnDB('SELECT VERSION();')
    return True


def create_DB():
    """
    Creates the database based on the metadata.
    @return: True if success else throws an error.
    """
    Base.metadata.create_all(dbEngine)
    print("The following tables have been deployed: ")
    for table in Base.metadata.tables.keys():
        print("\t" + table)

    return True


def delete_DB():
    """
    Deleting all the Data and the schema public of the database and then recreating the schema public
    @return: True if successful, else throws error
    """
    __executeSqlOnDB("DROP SCHEMA public CASCADE;")
    __executeSqlOnDB("CREATE SCHEMA public;")
    print("Schema has been deleted and recreated!")
    return True
