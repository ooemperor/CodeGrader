"""
Holds the Handlers for everything that corresponds with the Subject
@author: mkaiser
# TODO: Handle Errors while parsing information or querying the database
# TODO: Define and document proper response after put and post operations.

"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import Subject


class SubjectHandler(BaseHandler):
    """
    Handler for the Subject.
    Using the default get, post, delete and put methods defined in the BaseHandler
    @see: BaseHandler
    """
    def __init__(self):
        """
        Constructor for the ProfileHandler
        """
        super().__init__()
        self.dbClass = Subject
