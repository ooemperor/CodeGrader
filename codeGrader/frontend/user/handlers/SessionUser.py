# CodeGrader - https://github.com/ooemperor/CodeGrader
# Copyright © 2023, 2024 Michael Kaiser <michael.kaiser@emplabs.ch>
#
# This file is part of CodeGrader.
#
# CodeGrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CodeGrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CodeGrader.  If not, see <http://www.gnu.org/licenses/>.

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
        self.subjects = user_dict["memberships"]
        if self.profile is not None:
            self.profile_id = self.profile["id"]
            self.profile_name = self.profile["name"]
        else:
            self.profile_id = None
            self.profile_name = None

    def check_permission(self, profile_id: str = None, subject_id: str = None) -> bool:
        """
        Check the permission of the user for a given object and the corresponding profile and/or subject
        If the operation on the given profile is allowed we return true
        else we return false
        @param profile_id: The identifier of the profile
        @type profile_id: str
        @param subject_id: The id of a subject
        @type subject_id: int
        @return: True if the operation is allowed else false
        @rtype: bool
        """
        assert (profile_id is not None or subject_id is not None)

        profile_bool = False
        subject_bool = False

        if (profile_id == self.profile_id) or (profile_id is None):
            profile_bool = True

        if (subject_id in self.subjects) or (subject_id is None):
            print(subject_id)
            subject_bool = True
        return profile_bool and subject_bool

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
