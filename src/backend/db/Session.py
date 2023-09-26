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
    @see: src.backend.db.Base
    """

    def __init__(self):
        """
        Constructor for the session
        """
        # dbEngine is used from the db package
        self.session = sessionmaker(dbEngine)  # creating the session

    def create(self, instance):
        """
        Adding the instance into the database
        @param instance:
        @type instance: instance of type Base or any Subclass from Base
        @raise: raises any error that may occur in the Transaction.
        @return: True for success or else and Exception
        """
        try:
            with self.session.begin() as session:
                session.add(instance)
                session.commit()
        except Exception:
            session.rollback()
            raise

        return True

    def delete(self, instance):
        """
        Deleting an instance from the database
        @param instance: The object to delete from the database
        @type instance: instance of type Base or any Subclass from Base
        @raise: raises any error that may occur in the Transaction.
        @return: True for success or else and Exception
        """
        try:
            with self.session.begin() as session:
                session.delete(instance)
                session.commit()
        except Exception:
            session.rollback()
            raise

    def update(self, cls, identifier, update_dict):
        """
        Function for updating an object in the database
        @param cls: The class of the Object for the table mapping
        @type cls: type(object)
        @param identifier:
        @type identifier: BIGINT
        @param update_dict:
        @type update_dict: dict
        @return: True for succesful update
        @rtype: Boolean
        """
        try:
            with self.session.begin() as session:
                object_ = session.get(cls, identifier)
                object_.set_attrs(update_dict)
                session.commit()
                return True
        except Exception:
            session.rollback()
            raise

    def get_object(self, cls, identifier):
        """
        Get a object form the database using the given identifier
        @param cls: The class of the Object for the table mapping
        @type cls: type(object)
        @param identifier: The id of the object.
        @type identifier: BIGINT
        @return: The object form the database
        @rtype: cls
        """
        try:
            with self.session.begin() as session:
                object_ = session.get(cls, identifier)
                session.commit()
                return object_
        except Exception:
            session.rollback()
            raise




