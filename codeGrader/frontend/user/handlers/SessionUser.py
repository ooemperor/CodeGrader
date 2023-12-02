"""
Handlers Classes and more for Users from the user frontend
@author: mkaiser
"""

from .Base import BaseHandler
from flask_login import UserMixin


class SessionUser(UserMixin):
    """
    Representation of a User used for the CookieGeneration.
    """

    def __init__(self, user_id):
        """
        Constructor of the SessionUser Object
        @param user_id: The
        """

        user_dict = UserSessionHandler().get(user_id)
        self.id = user_dict["id"]
        self.username = user_dict["username"]
        self.first_name = user_dict["first_name"]
        self.last_name = user_dict["last_name"]
        self.profile = user_dict["profile"]


class UserSessionHandler(BaseHandler):
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
        print(id_)
        return self.api.get(f"/user/{id_}")
