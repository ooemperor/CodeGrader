"""
Holds the Handlers for everything that corresponds with the Users
@author: mkaiser
# TODO: Handle Errors while parsing information or querying the database
# TODO: Define and document proper response after put and post operations.
# TODO: Define how to handle realtions of Profile and more.

"""
from src.backend.handlers.Base import BaseHandler
from src.backend.db import User, AdminUser


class UserHandler(BaseHandler):
    """
    Handler for a UserObject
    """
    def get(self, id_):
        """
        Get a specific User from the database
        @param id_: the id of the user in the database
        @type id_: int
        @return: JSON representation of the object
        @rtype: str
        """
        assert (id_ is not None) and (id_ > 0)
        super().__init__()
        with self.sql_session.begin() as sql:
            user = sql.get(User, id_)
            sql.expunge(user)  # taking the user away from the session, so we can work on it away from DB.

        # TODO: Here we need to handle the error when no object can be found in the database.
        return user.get_attrs()

    def post(self, dict_):
        """
        Creating a new user object and writing in the database
        @param dict_: The dictionary/ key:value pair for the creation of the user
        @type dict_: dict
        @return: True else Error # TODO: Add more meaningful return Type
        @rtype: Boolean
        """
        super().__init__()
        user = User(dict_)
        with self.sql_session.begin() as sql:
            sql.add(user)
            sql.commit()
        return True  # TODO: Return has to be more precise

    def put(self, id_, dict_):
        """
        Updating a existing user in the database
        @param id_: The identifier of the object
        @type id_: int
        @param dict_: the arguments for the user that are updated
        @type dict_: key:value pairs
        @return: True or False depending on the outcome of the post. # TODO: will be further refined
        @rtype: Boolean
        """
        super().__init__()
        dict_id_ = dict[id]
        assert dict_id_ == id_

        with self.sql_session.begin() as sql:
            user = sql.get(User, id_)
            user.set_attrs(dict_)
            sql.commit()
        return True


