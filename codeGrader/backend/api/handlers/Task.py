"""
Holds the Handlers for everything that corresponds with the Task
@author: mkaiser
"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import Task


class TaskHandler(BaseHandler):
    """
    Handler for the Task.
    Using the default get, post, delete and put methods defined in the BaseHandler
    # TODO: integrate the files to be added.
    @see: BaseHandler
    """
    def __init__(self) -> None:
        """
        Constructor for the ProfileHandler
        """
        super().__init__()
        self.dbClass = Task
