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
        user = self.sql_session.get_object(User, identifier)
        # TODO: Here we need to handle the error when no object can be found in the database.
        # Maybe write the get function into the BaseHandler
        return True
