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
Handler Classes for the Home site of the user panel
"""
import flask
import flask_login
from flask import request, render_template, redirect
from .Base import BaseHandler


class HomeHandler(BaseHandler):
    """
    Handles Operations for the Home site
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the Home Handler
        @param request: The request from the app route of flask
        @type request: flask.request
        """
        super().__init__(request)

    def get(self):
        return render_template("home.html")
