"""
Base Handler for the backend API. Setting basic properties like a session.
@author: mkaiser
"""
from src.backend.db import Session


class BaseHandler:
    """
    The Class for the Basic Hanlder of the backend API.
    This Handler will be the parent class for all the other handlers.
    """

    def __init__(self):
        """
        Constructor of the BaseHandler
        Setting up Ojbects and params that we use in all handlers.
        @return: No return
        """
        self.sql_session = Session()  # creating the  session for later use
