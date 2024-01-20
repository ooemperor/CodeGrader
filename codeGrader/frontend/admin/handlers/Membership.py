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
Handler Classes for the Memberships in the admin frontend
@author: mkaiser
"""
import flask
from flask import render_template, redirect, url_for, Response
from .Base import BaseHandler
from typing import Union


class AddMembershipHandler(BaseHandler):
    """
    Handler Class for the creation of a Membership
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the AddMembership Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def post(self) -> Response:
        """
        Post Operation
        Creates the membership in the backend.
        @return: Redirect to the adminUsers Site
        """
        assert self.request.form is not None

        user_id = self.get_value("user")
        subject_id = self.get_value("subject")

        user = self.api.get(f"/user/{user_id}")
        subject = self.api.get(f"/subject/{subject_id}")

        if self.admin.check_permission('w', user["profile"]["id"]) and self.admin.check_permission('w', subject["profile"]["id"]):
            membership_data = dict()

            # getting the data from the form provided in the request
            membership_data["user_id"] = user_id
            membership_data["subject_id"] = subject_id

            self.api.post(f"/membership/add", body=membership_data)

        else:
            self.flash("You are not allowed to view this site. ")

        # either way redirect to the user page.
        return redirect(url_for("user", id_=user_id))


class DeleteMembershipHandler(BaseHandler):
    """
    Handler to delete a membership from the api backend
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the DeleteMembershipHandler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def post(self, id_: int) -> Response:
        """
        Post Operation for Membership Deletion
        Deletes the membership in the backend via an API Call
        @param id_: The identifier of the Membership
        @type id_: int
        @return: Redirection to the user site, where the membership has been deleted
        @rtype: Response
        """
        membership = self.api.get(f"/membership/{id_}")
        if self.admin.check_permission('w', membership["subject"]["profile"]["id"]):  # admin is allowed to delete the membership

            self.api.delete(f"/membership/{id_}")

            # display message that user has been deleted on the returned page.
            self.flash("Membership has been deleted")

        else:  # admin is not allowed to delete users
            self.flash("You are not allowed to delete Memberships. ")

        # either way we redirect to the user page
        return redirect(url_for("user", id_=membership["user"]["id"]))
