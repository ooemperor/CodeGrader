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
Handler Classes for the Error Sites of the CodeGrader
"""
import flask
import flask_login
from flask import request, render_template, redirect
from .Base import BaseHandler
import datetime
from codeGrader.frontend.config import config


class ErrorHandler(BaseHandler):
    """
    Handles Rendering of the Error Site
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the Error Handler
        @param request: The request from the app route of flask
        @type request: flask.request
        """
        super().__init__(request)

    def get(self, error: Exception, error_code: int) -> (str, int):
        """
        Renders the template of the Error Site of the user frontend
        @param error: The Exception of the site
        @type error: Exception
        @param error_code: The Error Code of the site
        @type error_code: int
        @return: str
        """
        request_data = dict()
        request_data["path"] = self.request.path
        request_data["method"] = self.request.method
        request_data["time"] = datetime.datetime.now()
        request_data["error"] = error

        if error_code == 404:
            request_data["title"] = "Page not found"
            request_data["error_text"] = "It looks like the page you are looking for does not exist"
            request_data["gif"] = config.gif_404
            return render_template("error.html", **request_data), error_code

        elif error_code == 500:
            request_data["title"] = f"{config.userAppName} not found"
            request_data["error_text"] = "An Error occured on the server while processing your request. Please Try Again!"
            request_data["gif"] = config.gif_500
            return render_template("error.html", **request_data), error_code

        else:
            request_data["title"] = f"{config.userAppName} Error"
            request_data["error_text"] = "Something went wrong. Please Try Again!"
            request_data["gif"] = config.gif_500
            return render_template("error.html", **request_data), error_code
