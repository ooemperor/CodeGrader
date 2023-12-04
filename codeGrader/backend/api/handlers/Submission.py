"""
Holds the Handlers for everything that corresponds with the Submission Class.
@author: mkaiser
"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import Submission


class SubmissionHandler(BaseHandler):
    """
    Handler for the Submission Class.
    Using the default get, post, delete and put methods defined in the BaseHandler
    @see: BaseHandler
    """
    def __init__(self) -> None:
        """
        Constructor for the ProfileHandler
        """
        super().__init__()
        self.dbClass = Submission

