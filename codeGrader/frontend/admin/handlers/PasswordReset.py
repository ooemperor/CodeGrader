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
Handler Class for the Resetting the password of a user in the admin frontend
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from typing import Union
import json


class PasswordResetHandler(BaseHandler):
    """
    Handler Class for the PasswordReset
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor for the handler of a PasswordReset
        @param request: The request provided by the routes file
        @type request: flask.Request
        @return: Nothing
        @rtype: None
        """
        super().__init__(request)

    def post(self, id_) -> Union[str, Response]:
        """
        Post method to reset the password of the user via an api call to the backend
        @return: The rendered site or a redirect
        @rtype: str|Response
        """

        user_before = self.api.get(f"/user/{id_}")  # get the user data
        if self.admin.check_permission('w', user_before["profile"]["id"]):
            user_data = dict()
            user_data["id"] = id_
            self.api.post(f"/user/{id_}/password/reset", body=user_data)

            self.flash(f"Password for the user has been reset and sent to user via Mail")

        else:  # admin is not allowed to update the user
            self.flash("You are not allowed to update this user")

        return redirect(url_for("user", id_=id_))
