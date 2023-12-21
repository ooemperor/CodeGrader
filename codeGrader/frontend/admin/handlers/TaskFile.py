"""
Handlers for the handling of the TaskFiles
@author: mkaiser
"""
import mimetypes

import flask
import requests
from flask import request, render_template, redirect, url_for, flash, Response, send_file, stream_with_context
from .Base import BaseHandler
from typing import Union
import io


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
            for file_key in self.request.files.keys():

                file = self.request.files[file_key]

                # upload the files to the backend api
                files = {file.filename: file}
                data = {"data": str({"task_id": id_, "file_id": 0})}  # file_id will be overwritten in the backend

                # constructing the url of the api call
                url = f"/task/{id_}/{self.fileObject}/add"

                self.api.post(url, data=data, files=files)

        else:  # admin is not allowed to access
            self.flash("You are not allowed to update this task")

        # either way redirect to the task
        return redirect(url_for("task", id_=id_))


class TaskFile(BaseHandler):
    """
    Handles the download (GET) Operation on a TaskFile (Attachment and Instruction)
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the TaskFile Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)
        self.fileObject = None

    def get(self, task_id_: int, task_file_id: int) -> Union[str, Response]:
        """
        Get and render the page for a given TaskFile by its id
        @param task_id_: The id of the Task
        @type task_id_: int
        @param task_file_id: The id of the TaskFile
        @type task_file_id: int
        @return: The File as a download
        @rtype: HTML
        """
        task = self.api.get(f"/task/{task_id_}")

        editable = self.admin.check_permission('w', task["profile"]["id"])

        if self.admin.check_permission('r', task["profile"]["id"]):  # when admin is allowed to view this File

            file_data = self.api.get(f"/task/{task_id_}/{self.fileObject}/{task_file_id}")
            file_id_ = file_data["file"]["id"]

            req = self.api.get_file(f"/file/{file_id_}")

            req.headers['Content-Disposition'] = 'attachment;filename=SmartFileName.txt'
            return Response(stream_with_context(req.iter_content(chunk_size=2048)),
                            content_type=req.headers["content-type"])

        else:  # admin is not allowed to view this task
            self.flash("You are not allowed to download this file. ")
            return redirect(url_for("task", id_=task_id_))


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

    def get(self, task_id_: int,  file_id_: int) -> Union[str, Response]:
        """
        Get Handler to render the site for confirmation for deletion of a Task
        @param task_id_: The id_ of the Task
        @type task_id_: int
        @param file_id_: The id_ of the TaskFile
        @type file_id_: int
        @return: Rendered Template
        """
        task = self.api.get(f"/task/{task_id_}")

        editable = self.admin.check_permission('w', task["profile"]["id"])

        taskfile = self.api.get(f"/task/{task_id_}/{self.fileObject}/{file_id_}")
        taskfile["task_id_"] = task_id_

        if editable:
            return render_template(self.templateName, **taskfile)  # TODO: Create the Template

        else:
            self.flash("You are not allowed to delete Files on this Task. ")
            return redirect(url_for("task", id_=task_id_))

    def post(self,task_id_: int,  file_id_: int) -> Response:
        """
        Post Operation for Task Deletion
        Deletes the task in the backend via an API Call
        @param task_id_: The idnentifier of the Task
        @type task_id_: int
        @param file_id_: The idnentifier of the File
        @type file_id_: int
        @return: Redirection to the Task table
        """
        task = self.api.get(f"/task/{task_id_}")
        if self.admin.check_permission('w', task["profile"]["id"]):  # admin is allowed to delete the task

            if self.get_value("action_button") == "Submit":
                self.api.delete(f"/task/{task_id_}/{self.fileObject}/{file_id_}")

                self.flash(f"{self.fileObject} has been deleted")
                return redirect(url_for("task", id_=task_id_))

            elif self.get_value("action_button") == "Cancel":
                return redirect(url_for("task", id_=task_id_))

            else:
                pass
                # TODO Implement Error

        else:  # admin is not allowed to delete tasks
            self.flash("You are not allowed to delete Files from tasks. ")
            return redirect(url_for("task", id_=task_id_))
