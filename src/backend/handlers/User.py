"""
Holds the Handlers for everything that corresponds with the Users
"""
from src.backend.handlers.Base import BaseHandler
from src.backend.db import User, AdminUser


class UserHandler(BaseHandler):
    """
    Handler for a UserObject
    """
    def get(self, identifier):
        """
        Get a specific User from the database
        @param identifier: the id of the object in the database
        @type identifier: int
        @return: JSON representation of the object
        @rtype: str
        """
        super().__init__()
        with self.sql_session.begin() as sql:
            user = sql.get(User, identifier)
            sql.expunge(user)  # taking the user away from the session, so we can work on it away from DB.

        # TODO: Here we need to handle the error when no object can be found in the database.
        return user.get_attrs()

    def post(self, **kwargs):
        """
        updating the single user in the database.

        @param kwargs: the arguments for the user that are updated
        @type kwargs: key:value pairs
        @return: True or False depending on the outcome of the post. # TODO: will be further refined
        @rtype: Boolean
        """
        return True

