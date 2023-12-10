"""
Handlers for the handling of the TaskInstructions
Inherits from the TaskFile Classes
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from .TaskFile import AddTaskFile, DeleteTaskFile
from typing import Union


class AddTaskInstruction(AddTaskFile):
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
        self.fileObject = "Instruction"


class DeleteTaskInstruction(DeleteTaskFile):
    """
    Handler to delete a TaskInstruction from the api backend
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the DeleteTaskInstruction Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)
        self.templateName = "DeleteTaskInstruction.html"
        self.fileObject = "Instruction"
