"""
Handlers for the handling of the TaskAttachments
Inherits from the TaskFile Classes
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from .TaskFile import AddTaskFile, DeleteTaskFile, TaskFile
from typing import Union


class AddTaskAttachmentHandler(AddTaskFile):
    """
    Handles the operation on a TaskAttachment
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the Attachment Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)
        self.fileObject = "attachment"


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


class DeleteTaskAttachmentHandler(DeleteTaskFile):
    """
    Handler to delete a Task from the api backend
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the DeleteTaskAttachment Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)
        self.templateName = "deleteTaskAttachment.html"
        self.fileObject = "attachment"




