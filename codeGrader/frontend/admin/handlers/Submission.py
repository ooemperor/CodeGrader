"""
File for the Handlers for Submissions
@author: mkaiser
"""

import flask
import requests
from flask import request, render_template, redirect, url_for, flash, Response, send_file, stream_with_context
from .Base import BaseHandler
from typing import Union
import io


class SubmissionFileHandler(BaseHandler):
    """
    Handles the download (GET) Operation on a TaskFile (Attachment and Instruction)
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the SubmissionFile Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get and render the page for a given TaskFile by its id
        @param id_: The id of the Submission
        @type id_: int
        @return: The File as a download
        @rtype: HTML
        """
        submission = self.api.get(f"/submission/{id_}")
        task_id = submission["task"]["profile"]["id"]

        if self.admin.check_permission('r', task_id):  # when admin is allowed to view this File
            file_id = submission["file_id"]

            req = self.api.get_file(f"/file/{file_id}")
            filename = submission["file"]["filename"]
            req.headers['Content-Disposition'] = f"attachment;filename={filename}"
            return Response(stream_with_context(req.iter_content(chunk_size=2048)),
                            content_type=req.headers["content-type"])

        else:  # admin is not allowed to view this task
            self.flash("You are not allowed to download this file. ")
            return redirect(url_for("task", id_=task_id))
