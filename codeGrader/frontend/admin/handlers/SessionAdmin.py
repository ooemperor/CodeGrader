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
            self.profile_id = self.profile["id"]
            self.profile_name = self.profile["name"]
        else:
            self.profile_id = None
            self.profile_name = None
        self.type = user_dict["admin_type"]
        self._admin_type_name = self.type["name"]

    def check_permission(self, operation: str, profile_id: str = None, create_object: str = None) -> bool:
        """
        Check the permission of the admin for a given Operation and profile
        If the operation on the given profile is allowed we return true
        else we return false
        @param operation: r or w r == Read w == Write
        @type operation: str
        @param profile_id:
        @type profile_id: str
        @param create_object: What type of object we want to create
        @type create_object: str
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

            elif profile_id == self.profile_id:
                # checking if the profile is allowed
                return True

            else:
                return False

        elif operation == 'w':
            if self._admin_type_name == config.admin_rw_partial and profile_id == self.profile_id:
                return True

            elif self._admin_type_name == config.admin_rw_partial and create_object not in [None, "profile", "admin"]:
                return True

            else:
                return False

        else:
            raise Exception("Unsupported operation type. \n Only r and w for read and write are allowed")

    def get_filter_profile(self) -> str:
        """
        Construct the filter string for the API Call to the backend
        @return: The string that needs to be appended to the filtering
        @rtype: str
        """
        if self._admin_type_name in [config.admin_rw_full, config.admin_r_full]:
            return ""

        elif self._admin_type_name in [config.admin_rw_partial, config.admin_r_partial]:
            return f"{self.profile}"

    def get_filter_profile_name(self) -> str:
        """
        Construct the filter string for the API Call to the backend
        @return: The string that needs to be appended to the filtering
        @rtype: str
        """
        if self._admin_type_name in [config.admin_rw_full, config.admin_r_full]:
            return ""

        elif self._admin_type_name in [config.admin_rw_partial, config.admin_r_partial]:
            return self.profile_name


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
