"""
Holds the Handlers for everything that corresponds with the Users
@author: mkaiser
# TODO: Define how to handle realtions of Profile and more.
"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import User, AdminUser


class UserHandler(BaseHandler):
    """
    Handler for a UserObject
    """

    def __init__(self):
        """
        Constructor for the UserHandlerClass
        """
        super().__init__()
        self.dbClass = User


class AdminUserHandler(BaseHandler):
    """
    Handler for the AdminUser
    """

    def __init__(self):
        """
        Constructor for the UserHandlerClass
        """
        super().__init__()
        self.dbClass = AdminUser
