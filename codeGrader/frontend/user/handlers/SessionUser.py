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
        if self.profile is not None:
            self.profile_id = self.profile["id"]
            self.profile_name = self.profile["name"]
        else:
            self.profile_id = None
            self.profile_name = None

    def check_permission(self, profile_id: str = None) -> bool:
        """
        Check the permission of the user for a given object and the corresponding profile
        If the operation on the given profile is allowed we return true
        else we return false
        @param profile_id: The identifier of the profile
        @type profile_id: str
        @return: True if the operation is allowed else false
        @rtype: bool
        """
        if profile_id == self.profile_id:
            return True

        else:
            return False

    def get_filter_profile(self) -> str:
        """
        Construct the filter string for the API Call to the backend
        @return: The string that needs to be appended to the filtering
        @rtype: str
        """
        return f"{self.profile}"


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
        return self.api.get(f"/user/{id_}")
