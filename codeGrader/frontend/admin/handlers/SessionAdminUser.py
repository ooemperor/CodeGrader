"""
Handlers Classes and more for Users from the admin frontend
@author: mkaiser
"""

from .Base import BaseHandler
from flask_login import UserMixin
import json


class SessionAdminUser(UserMixin):
    """
    Representation of a AdminUser used for the CookieGeneration.
    """

    def __init__(self, adminUser_id):
        """
        Constructor of the SessionUser Object
        @param adminUser_id: The
        """

        user_dict = AdminUserHandler().get(adminUser_id)
        self.id = user_dict["id"]
        self.username = user_dict["username"]


class AdminUserHandler(BaseHandler):
    """
    UserHandler
    Handles all the operations that can be done on a User in the backend
    """

    def __init__(self):
        """
        Constructor of the UserHandler
        """
        super().__init__(requests=None)

    def get(self, id_: int):
        """
        Get the representation of a user by its id.
        @param id_: The id of the user
        @type id_: int
        @return: The User as a json representation
        """
        return self.api.get(f"/adminUser/{id_}")




