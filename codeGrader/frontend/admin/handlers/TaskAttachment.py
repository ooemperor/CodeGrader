"""
Handlers for the handling of the TaskAttachments
Inherits from the TaskFile Classes
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from .TaskFile import AddTaskFile, DeleteTaskFile
from typing import Union


class AddTaskAttachment(AddTaskFile):
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
        self.fileObject = "Attachment"


class DeleteTaskAttachment(DeleteTaskFile):
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
        self.templateName = "DeleteTaskAttachment.html"
        self.fileObject = "Attachment"




