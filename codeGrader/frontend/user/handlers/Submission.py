"""
Handler Class for the Submission for a given task.
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from typing import Union


class AddSubmissionHandler(BaseHandler):
    """
    Class to handle the upload of an submission
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the Handler
        """
        super().__init__(request)

    def post(self, id_: int) -> Response:
        """
        Handler for adding a Submission to a task for a user
        @param id_: The identifier of the task
        @return:
        """
        assert self.request.form is not None
        assert self.request.files is not None

        user_id = self.user.id
        task_id = id_

        for file_key in self.request.files.keys():
            file = self.request.files[file_key]

            # upload the files to the backend api
            files = {file.filename: file}
            # constructing the url of the api call
            url = f"/file/upload"
            resp = self.api.post(url, files=files)  # uploading the file and retreiving response body

            file_id = resp["response"]["id"]
            body = ({"task_id": task_id, "file_id": file_id, "user_id": user_id})
            url = f"/submission/add"

            self.api.post(url, body=body)  # adding the submission via file_id

        # either way redirect to the task
        self.flash("Submission received")
        return redirect(url_for("task", id_=id_))
