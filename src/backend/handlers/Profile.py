"""
Holds the Handlers for everything that corresponds with the Profile
@author: mkaiser
# TODO: Handle Errors while parsing information or querying the database
# TODO: Define and document proper response after put and post operations.

"""
from src.backend.handlers.Base import BaseHandler
from src.backend.db import Profile


class ProfileHandler(BaseHandler):
    """
    Handler for the Profile.
    Using the default get, post, delete and put methods defined in the BaseHandler
    @see: BaseHandler
    """
    def __init__(self):
        """
        Constructor for the ProfileHandler
        """
        super().__init__()
        self.dbClass = Profile
