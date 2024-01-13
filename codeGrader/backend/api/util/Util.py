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
File that contains util methods for the main flask app class
@author: mkaiser
"""
import flask

from codeGrader.backend.api.handlers import FileHandler
from flask import request
import json


def upload_file(request) -> dict:
    """
    Private Method to be only used within this class to upload a file.
    @param request: The request that has been made to the api
    @type request: Request
    @return: Custom Response message that we get from the handler class.
    @rtype: dict
    """
    if len(request.files.keys()) > 1:  # only allow one file at a tim
        return "Error", 500

    else:
        file_ = request.files[list(request.files.keys())[0]]
        file_type = file_.name.rsplit('.', 1)[1].lower()
        data = {"filename": file_.name, "fileExtension": file_type, "file": file_.read()}
        return FileHandler().post(data)


def preprocess_task_file(request: flask.Request) -> dict:
    """
    Preprocesses a request for Attachments and Instructions on a Task
    uploads a file via other method
    @param request: The Flask request received by the app
    @type
    @return:
    """
    file_response = upload_file(request)[0]
    file_id = file_response["response"]["id"]
    file_data = request.form.to_dict()
    file_data = json.loads(file_data["data"].replace("\'", "\""))
    file_data['file_id'] = int(file_id)
    return file_data
