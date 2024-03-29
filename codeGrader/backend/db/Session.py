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
Script to store the session Class that manipulates the database
@author: mkaiser
"""
from . import dbEngine
from sqlalchemy.orm import sessionmaker


class Session:
    """
    The Session class is the owner of the operations which are done on the Database.
    No Object or application logic shall be stored within session. Only technical logic.
    Updating a object in the database is handled on the object.
    @see: codeGrader.backend.db.Base
    """
    def __init__(self):
        """
        Constructor for the session
        """
        # dbEngine is used from the db package
        self.session = sessionmaker(dbEngine)  # creating the session

    def create(self, object_: object) -> int:
        """
        Adding the instance into the database
        @param object_: The Object that we want to create.
        @type object_: instance of type Base or any Subclass from Base
        @raise: raises any error that may occur in the Transaction.
        @return: True
        """
        try:
            with self.session.begin() as session:
                session.add(object_)
                session.flush()  # creating object in DB
                session.refresh(object_)  # refreshing the object from db
                return_id = object_.id  #definition of the id of the newly created object
                session.commit()  # finally commit the session.
        except Exception:
            session.rollback()
            raise
        return return_id

    def delete(self, object_: object) -> bool:
        """
        Deleting an instance from the database
        @param object_: The object to delete from the database
        @type object_: instance of type Base or any Subclass from Base
        @raise: raises any error that may occur in the Transaction.
        @return: True for success or else and Exception
        @rtype: bool
        """
        try:
            with self.session.begin() as session:
                session.delete(object_)
                session.commit()
                return True

        except Exception:
            session.rollback()
            raise

    def delete(self, cls: type, id_: int) -> bool:
        """
        Deleting a object from the database by id and Class
        @param cls: The Class of the Object
        @type cls: type
        @param id_: The identifier of the object in the database
        @type id_: int
        @return:
        """
        try:
            with self.session.begin() as session:
                session.delete(session.get(cls, id_))
                session.commit()
                return True

        except Exception:
            session.rollback()
            raise

    def update(self, cls: type, id_: int, update_dict: dict) -> bool:
        """
        Function for updating an object in the database
        @param cls: The class of the Object for the table mapping
        @type cls: type(object)
        @param id_:
        @type id_: BIGINT
        @param update_dict:
        @type update_dict: dict
        @return: True for succesful update
        @rtype: bool
        """
        try:
            with self.session.begin() as session:
                object_ = session.get(cls, id_)
                object_.set_attrs(update_dict)
                session.commit()
                return True
        except Exception:
            session.rollback()
            raise

    def get_object(self, cls: type, id_: int) -> type:
        """
        Get a object form the database using the given identifier
        @param cls: The class of the Object for the table mapping
        @type cls: type(object)
        @param id_: The id of the object.
        @type id_: BIGINT
        @return: The object from the database
        @rtype: type
        """
        try:
            with self.session.begin() as session:
                object_ = session.query(cls).get(id_)
                session.expunge(object_)
                session.expunge_all()
                return object_
        except Exception as e:
            session.rollback()
            raise

    def get_all(self, cls: type) -> list:
        """
        Get all objects for a given instance.
        @param cls: The class of the Object for the table mapping
        @type cls: type(object)
        @return: The objects from the database
        @rtype: list
        """
        try:
            with self.session.begin() as session:
                objects_ = session.query(cls).all()
                session.expunge_all()
                return objects_
        except Exception as error:
            print(error)
            session.rollback()
            raise
