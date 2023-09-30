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
    # TODO: need more meaningful error messages.
    def __init__(self):
        """
        Constructor for the session
        """
        # dbEngine is used from the db package
        self.session = sessionmaker(dbEngine)  # creating the session

    def create(self, object_):
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
                session.refresh(object_) # refreshing the object from db
                return_id = object_.id  #definition of the id of the newly created object
                session.commit() # finally commit the session.
        except Exception:
            session.rollback()
            raise

        return return_id

    def delete(self, object_):
        """
        Deleting an instance from the database
        @param object_: The object to delete from the database
        @type object_: instance of type Base or any Subclass from Base
        @raise: raises any error that may occur in the Transaction.
        @return: True for success or else and Exception
        """
        try:
            with self.session.begin() as session:
                session.delete(object_)
                session.commit()
        except Exception:
            session.rollback()
            raise

    def delete(self, cls, id_):
        try:
            with self.session.begin() as session:
                session.delete(session.get(cls, id_))
                session.commit()
        except Exception:
            session.rollback()
            raise

    def update(self, cls, id_, update_dict):
        """
        Function for updating an object in the database
        @param cls: The class of the Object for the table mapping
        @type cls: type(object)
        @param id_:
        @type id_: BIGINT
        @param update_dict:
        @type update_dict: dict
        @return: True for succesful update
        @rtype: Boolean
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

    def get_object(self, cls, id_):
        """
        Get a object form the database using the given identifier
        @param cls: The class of the Object for the table mapping
        @type cls: type(object)
        @param id_: The id of the object.
        @type id_: BIGINT
        @return: The object form the database
        @rtype: cls
        """
        try:
            with self.session.begin() as session:
                object_ = session.query(cls).get(id_)
                session.expunge(object_)
                return object_
        except Exception:
            session.rollback()
            raise




