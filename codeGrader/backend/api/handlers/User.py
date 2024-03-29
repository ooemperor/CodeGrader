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
Holds the Handlers for everything that corresponds with the Users
@author: mkaiser
# TODO: Define how to handle realtions of Profile and more.
"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import User
import hashlib


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

    def _preprocess_data_dict(self, dict_: dict) -> dict:
        """
        Preprocessing of the data dictionary for the User Handler
        Overwrites the method from the parent class
        Hashes the value of the password
        @param dict_: The data dictionary used for put or post of the object
        @type dict_: dict
        @return: The preprocessed dictionary
        @rtype: dict
        """
        if "password" in dict_.keys():
            password = dict_["password"]
            password = password.encode('utf-8')
            hash_object = hashlib.sha256(password)
            hex_dig = hash_object.hexdigest()
            dict_["password"] = hex_dig

        return dict_
