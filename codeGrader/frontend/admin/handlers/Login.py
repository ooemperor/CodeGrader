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
Login Page Handler
@author: mkaiser
"""
import flask
import json

from flask import Response

from .Base import BaseHandler


class AdminUserLoginHandler(BaseHandler):
    """
    Login Handler for the admin frontend
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the AdminUser Login Handler
        @param request: The request from the app route of flask
        @type request: flask.request
        """
        super().__init__(request)

    def post(self) -> Response:
        """
        Trying the authentication of the AdminUser via BackendAPI
        @return: User id_ if the credentials have been correct
        @rtype: int
        """

        username = self.request.form["username"]
        password = self.request.form["password"]
        body = dict()
        body["password"] = password
        body["username"] = username
        response = self.api.post('/admin/login', body)
        id_ = response["response"]["id"]  # is None when the Authentication failed
        return id_
