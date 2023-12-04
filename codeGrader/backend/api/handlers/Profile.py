"""
Holds the Handlers for everything that corresponds with the Profile
@author: mkaiser
"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import Profile


class ProfileHandler(BaseHandler):
    """
    Handler for the Profile.
    Using the default get, post, delete and put methods defined in the BaseHandler
    @see: BaseHandler
    """
    def __init__(self) -> None:
        """
        Constructor for the ProfileHandler
        """
        super().__init__()
        self.dbClass = Profile
