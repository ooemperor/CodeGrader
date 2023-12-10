"""
Handlers for the handling of the TaskFiles
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from typing import Union


class AddTaskFile(BaseHandler):
    """
    Handles the operation on a single task
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the File Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)
        self.fileObject = None

    def post(self, id_: int) -> Response:
        """
        Handler for adding an File to the task
        @param id_: The identifier of the task
        @return:
        """
        assert self.request.form is not None
        assert self.request.files is not None

        task_before = self.api.get(f"/task/{id_}")  # get the task data
        if self.admin.check_permission('w', task_before["profile"]["id"]):

            for file in self.request.files:
                # upload the files to the
                # TODO: implement the uplaod
                raise NotImplementedError

        else:  # admin is not allowed
            self.flash("You are not allowed to update this task")

        # either way redirect to the task
        return redirect(url_for("task", id_=id_))


class DeleteTaskFile(BaseHandler):
    """
    Handler to delete a Task from the api backend
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the DeleteTaskHandler Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)
        self.templateName = None
        self.fileObject = None

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get Handler to render the site for confirmation for deletion of a Task
        @param id_: The id_ of the task
        @type id_: int
        @return: Rendered Template
        """
        task = self.api.get(f"/task/{id_}")

        editable = self.admin.check_permission('w', task["profile"]["id"])

        if editable:
            return render_template(self.templateName, **task)  # TODO: Create the Template

        else:
            self.flash("You are not allowed to delete Files on this Task. ")
            return redirect(url_for("tasks"))

    def post(self, id_: int) -> Response:
        """
        Post Operation for Task Deletion
        Deletes the task in the backend via an API Call
        @param id_: The idnentifier of the Task
        @type id_: int
        @return: Redirection to the Task table
        """
        task = self.api.get(f"/task/{id_}")
        if self.admin.check_permission('w', task["profile"]["id"]):  # admin is allowed to delete the task

            if self.get_value("action_button") == "Submit":
                # TODO: Implement Deletion
                raise NotImplementedError

            elif self.get_value("action_button") == "Cancel":
                return redirect(url_for("task", id_=id_))

            else:
                pass
                # TODO Implement Error

        else:  # admin is not allowed to delete tasks
            self.flash("You are not allowed to delete Files from tasks. ")
            return redirect(url_for("task", id_=id_))


