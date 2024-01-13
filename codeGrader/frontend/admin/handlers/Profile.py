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
Handlers for the rendering of profiles
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from typing import Union


class ProfileListHandler(BaseHandler):
    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the ProfileListHandler
        Will Render the HTML Template for all the profiles.
        """
        super().__init__(request)

    def get(self) -> str:
        """
        Renders the template for the Profiles site.
        @return: The rendered template
        @rtype: HTML
        """
        profiles = self.api.get("/profiles", name=self.admin.get_filter_profile_name())
        return render_template("profiles.html", **profiles, this=self)


class ProfileHandler(BaseHandler):
    """
    Handles the operation on a single Profile
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the Profile Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get and render the page for a given profile by its id
        @param id_: The id of the profile
        @type id_: int
        @return: The rendered page of the profile
        @rtype: HTML
        """
        profile = self.api.get(f"/profile/{id_}")
        editable = self.admin.check_permission('w', profile["id"])  # checking if admin has write rights
        profile["editable"] = editable  # adding the rights to the render params

        if self.admin.check_permission('r', profile["id"]):  # when admin is allowed to view this profile
            return render_template("profile.html", **profile)

        else:  # admin is not allowed to view this profile
            self.flash("You are not allowed to view this profile. ")
            return redirect(url_for("profiles"))

    def post(self, id_: int) -> Response:
        """
        Handler for the update of a Profile
        @param id_: The identifier of the profile
        @return:
        """
        assert self.request.form is not None
        profile_before = self.api.get(f"/profile/{id_}")  # get the profile data

        if self.admin.check_permission('w', profile_before["id"]): # admin is allowed to update
            profile_data = dict()

            profile_data["name"] = self.get_value("name")
            profile_data["tag"] = self.get_value("tag")

            # getting the data from the form provided in the request
            self.api.put(f"/profile/{id_}", body=profile_data)

        else:
            self.flash("You are not allowed to update this profile! ")

        # either way redirect back to the profile
        return redirect(url_for("profile", id_=id_))


class AddProfileHandler(BaseHandler):
    """
    Class to handle the operations of creating a profile.
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the AddProfile Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self) -> str:
        """
        Render the template for adding
        @return: The rendered page
        """
        if self.admin.check_permission('w'): # check if admin has general write permission
            return render_template("addProfile.html")

        else: # admin has no write permission
            self.flash("You are not allowed to access this site! ")
            return redirect(url_for("profiles"))

    def post(self) -> Response:
        """
        Post Operation
        get the data out of the request and create the profile in the backend via api
        @return: redirect to another page
        """
        if self.admin.check_permission('w'): # admin has write permission to create profile
            profile_data = dict()

            profile_data["name"] = self.get_value("name")
            profile_data["tag"] = self.get_value("tag")

            self.api.post("/profile/add", body=profile_data)

        else: # admin does not have write permission
            self.flash("You are not allowed to view this site. ")

        # either way redirect back to profiles site
        return redirect(url_for("profiles"))


class DeleteProfileHandler(BaseHandler):
    """
    Handler to delete a Profile from the api backend
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the DeleteProfileHandler Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> str:
        """
        Get Handler to render the site for confirmation for deletion of a Profile
        @param id_: The id_ of the Profile
        @type id_: int
        @return: Rendered Template
        """
        profile = self.api.get(f"/profile/{id_}")

        editable = self.admin.check_permission('w', profile["id"])

        if editable:
            return render_template("deleteProfile.html", **profile)

        else:
            self.flash("You are not allowed to delete profiles. ")
            return redirect(url_for("profiles"))

    def post(self, id_: int) -> Response:
        """
        Post Operation for Profile Deletion
        Deletes the task in the backend via an API Call
        @param id_: The idnentifier of the Profile
        @type id_: int
        @return: Redirection to the Profile table
        """

        profile = self.api.get(f"/profile/{id_}")
        if self.admin.check_permission('w'):  # admin is allowed to delete the profile
            if self.get_value("action_button") == "Submit":
                response = self.api.delete(f"/profile/{id_}")

                # display message that Profile has been deleted on the returned page.
                self.flash("Profile has been deleted")
                return redirect(url_for("profiles"))

            elif self.get_value("action_button") == "Cancel":
                return redirect(url_for("profile", id_=id_))

            else:
                pass
                # TODO Implement Error

        else:  # admin is not allowed to delete profiles
            self.flash("You are not allowed to delete profiles. ")
            return redirect(url_for("profiles"))
