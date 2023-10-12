"""
Holds the Handlers for posting and getting a file.
@author: mkaiser
"""
from .Base import BaseHandler
from codeGrader.backend.db import File


class FileHandler(BaseHandler):
    """
    Handler for the File class.
    """
    def __init__(self):
        """
        Constructor for the FileHandler
        """
        super().__init__()
        self.dbClass = File

