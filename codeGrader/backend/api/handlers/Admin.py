"""
Holds the Handlers for everything that corresponds with the Users
@author: mkaiser
# TODO: Define how to handle realtions of Profile and more.
"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import User, AdminUser
import hashlib


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

    def _preprocess_data_dict(self, dict_: dict):
        """
        Preprocessing of the data dictionary for the Admin UserHandler
        Overwrites the method from the parent class
        Hashes the value of the password
        @param dict_: The data dictionary used for put or post of the object
        @type dict_: dict
        @return: The preprocessed dict
        @rtype: dict
        """
        if "password" in dict_.keys():
            password = dict_["password"]
            password = password.encode('utf-8')  # Convert the password to bytes
            hash_object = hashlib.sha256(password)  # Choose a hashing algorithm (e.g., SHA-256)
            hex_dig = hash_object.hexdigest()
            dict_["password"] = hex_dig

        return dict_
