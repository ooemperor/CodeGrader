# CodeGrader - https://github.com/ooemperor/CodeGrader
# Copyright © 2023, 2024 Michael Kaiser <michael.kaiser@emplabs.ch>
#
# This file is part of CodeGrader.
#
# CodeGrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CodeGrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CodeGrader.  If not, see <http://www.gnu.org/licenses/>.

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

        if self.user.check_permission(task["profile"]["id"]):  # when admin is allowed to view this File

            file_data = self.api.get(f"/task/{task_id_}/{self.fileObject}/{task_file_id}")
            file_id_ = file_data["file"]["id"]

            req = self.api.get_file(f"/file/{file_id_}")

            req.headers['Content-Disposition'] = 'attachment;filename=SmartFileName.txt'
            return Response(stream_with_context(req.iter_content(chunk_size=2048)),
                            content_type=req.headers["content-type"])

        else:  # admin is not allowed to view this task
            self.flash("You are not allowed to download this file. ")
            return redirect(url_for("task", id_=task_id_))
