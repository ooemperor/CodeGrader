"""
Handlers for the handling of the TaskAttachments
Inherits from the TaskFile Classes
@author: mkaiser
"""

import flask
from .TaskFile import TaskFile


class TaskAttachmentHandler(TaskFile):
    """
        Handles the operation on a TaskAttachment GET, Delete
        """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the Attachment Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)
        self.fileObject = "attachment"
