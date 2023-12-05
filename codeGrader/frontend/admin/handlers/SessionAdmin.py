"""
Handlers Classes and more for Users from the admin frontend
@author: mkaiser
"""

from .Base import BaseHandler
from flask_login import UserMixin
from codeGrader.frontend.config import config
import json


class SessionAdmin(UserMixin):
    """
    Representation of a AdminUser used for the CookieGeneration.
    """

    def __init__(self, adminUser_id) -> None:
        """
        Constructor of the SessionUser Object
        Setting need values on the user object.
        @param adminUser_id: The
        """

        user_dict = AdminSessionHandler().get(adminUser_id)
        self.id = user_dict["id"]
        self.username = user_dict["username"]
        self.profile = user_dict["profile"]
        if self.profile is not None:
            self._profile_name = self.profile["name"]
        else:
            self._profile_name = None
        self.type = user_dict["admin_type"]
        self._admin_type_name = self.type["name"]

    def check_permission(self, operation: str, profile_name: str) -> bool:
        """
        Check the permission of the admin for a given Operation and profile
        If the operation on the given profile is allowed we return true
        else we return false
        @param operation: r or w r == Read w == Write
        @type operation: str
        @param profile_name:
        @type profile_name: str
        @return: True if the operation is allowed else false
        @rtype: bool
        """

        if self._admin_type_name == config.admin_rw_full:
            # All Permissions are allowed so we return true
            # Admin is Super Admin
            return True

        if operation == 'r':
            if self._admin_type_name == config.admin_r_full:
                # it is a full read admin, so it is allowed
                return True

            elif profile_name == self._profile_name:
                # checking if the profile is allowed
                return True

            else:
                return False

        elif operation == 'w':
            if profile_name == self._profile_name and self._admin_type_name == config.admin_rw_partial:
                return True
            else:
                return False

        else:
            raise Exception("Unsupported operation type. \n Only r and w for read and write are allowed")

    def get_profile_filter(self) -> str:
        """
        Construct the filter string for the API Call to the backend
        @return: The string that needs to be appended to the filtering
        @rtype: str
        """
        if self._admin_type_name in [config.admin_rw_full, config.admin_r_full]:
            return ""

        elif self._admin_type_name in [config.admin_rw_partial, config.admin_r_partial]:
            return f"?profile={self.profile}"


class AdminSessionHandler(BaseHandler):
    """
    UserHandler
    Handles all the operations that can be done on a User in the backend
    """

    def __init__(self) -> None:
        """
        Constructor of the UserHandler
        """
        super().__init__(requests=None)

    def get(self, id_: int) -> str:
        """
        Get the representation of a user by its id.
        @param id_: The id of the user
        @type id_: int
        @return: The User as a json representation
        """
        return self.api.get(f"/admin/{id_}")
