"""
Handlers for the handling of the TaskInstructions
Inherits from the TaskFile Classes
@author: mkaiser
"""

import flask
from .TaskFile import TaskFile


class TaskInstructionHandler(TaskFile):
    """
    Handles the operation on TaskInstructions
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the Attachment Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)
        self.fileObject = "instruction"
