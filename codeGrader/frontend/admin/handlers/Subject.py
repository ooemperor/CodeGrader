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
Handlers for the rendering of Subjects
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from typing import Union


class SubjectListHandler(BaseHandler):
    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the SubjectListHandler
        Will Render the HTML Template for all the subjects.
        """
        super().__init__(request)

    def get(self) -> str:
        """
        Renders the template for the Subjects site.
        @return: The rendered template
        @rtype: HTML
        """
        subjects = self.api.get("/subjects", profile=self.admin.get_filter_profile())
        return render_template("subjects.html", **subjects, this=self)


class SubjectHandler(BaseHandler):
    """
    Handles the operation on a single Subject
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the Subject Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get and render the page for a given subject by its id
        @param id_: The id of the subject
        @type id_: int
        @return: The rendered page of the subject
        @rtype: HTML
        """
        subject = self.api.get(f"/subject/{id_}")
        profiles = self.api.get(f"/profiles", name=self.admin.get_filter_profile_name())  # get the profile data
        memberships = self.api.get(f"/memberships", subject_id=id_)
        subject_profile = subject["profile"]
        profile_users = self.api.get(f"/users", profile=subject_profile)
        profile_user_ids = []
        for user in profile_users["user"]:
            profile_user_ids.append(user["id"])

        subject["profiles"] = profiles["profile"]
        subject["memberships"] = memberships["membership"]

        scores = self.api.get(f"/scores/subject", object_id=id_)
        scores_prep = scores["subject"][0][str(id_)]
        scores = []
        for score in scores_prep:
            if score["user_id"] in profile_user_ids:
                scores.append(score)

        subject["scores"] = scores

        editable = self.admin.check_permission('w', subject["profile"]["id"])
        subject["editable"] = editable

        if self.admin.check_permission('r', subject["profile"]["id"]):  # when admin is allowed to view this user
            return render_template("subject.html", **subject)

        else:  # admin is not allowed to view this subject
            self.flash("You are not allowed to view this subject. ")
            return redirect(url_for("subjects"))

    def post(self, id_: int) -> Response:
        """
        Handler for the update of a subject
        @param id_: The identifier of the subject
        @return:
        """
        assert self.request.form is not None
        subject_before = self.api.get(f"/subject/{id_}")  # get the subject data
        if self.admin.check_permission('w', subject_before["profile"]["id"]):
            subject_data = dict()

            subject_data["name"] = self.get_value("name")
            subject_data["tag"] = self.get_value("tag")

            subject_data["profile_id"] = self.get_value("profile")

            # getting the data from the form provided in the request
            self.api.put(f"/subject/{id_}", body=subject_data)

        else:
            self.flash("You are not allowed to update this subject! ")

        # either way redirect back to the subject
        return redirect(url_for("subject", id_=id_))


class AddSubjectHandler(BaseHandler):
    """
    Class to handle the operations of creating a subject.
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the AddSubject Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self) -> Union[str, Response]:
        """
        Render the template for adding
        @return: The rendered page
        """
        if self.admin.check_permission('w', create_object="subject"):
            subject_data = dict()

            profiles = self.api.get(f"/profiles", name=self.admin.get_filter_profile_name())

            subject_data["profiles"] = profiles["profile"]

            return render_template("addSubject.html", **subject_data)

        else:  # admin is not allowed to view this subject
            self.flash("You are not allowed to access this site! ")
            return redirect(url_for("subjects"))

    def post(self) -> Response:
        """
        Post Operation
        get the data out of the request and create the subject in the backend via api
        @return: redirect to another page
        """

        if self.admin.check_permission('w', create_object='subject'):
            subject_data = dict()

            subject_data["name"] = self.get_value("name")
            subject_data["tag"] = self.get_value("tag")

            subject_data["profile_id"] = self.get_value("profile")

            self.api.post("/subject/add", body=subject_data)

        else:
            self.flash("You are not allowed to view this site. ")

        # either way redirect to the subjects site.
        return redirect(url_for("subjects"))


class DeleteSubjectHandler(BaseHandler):
    """
    Handler to delete a Subject from the api backend
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the DeleteSubjectHandler Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get Handler to render the site for confirmation for deletion of a Subject
        @param id_: The id_ of the Subject
        @type id_: int
        @return: Rendered Template
        """
        subject = self.api.get(f"/subject/{id_}")
        editable = self.admin.check_permission('w', subject["profile"]["id"])

        if editable:
            return render_template("deleteSubject.html", **subject)

        else:
            self.flash("You are not allowed to delete subjects. ")
            return redirect(url_for("subjects"))

    def post(self, id_: int) -> Response:
        """
        Post Operation for Subject Deletion
        Deletes the subject in the backend via an API Call
        @param id_: The idnentifier of the Subject
        @type id_: int
        @return: Redirection to the Subject table
        """
        subject = self.api.get(f"/subject/{id_}")
        if self.admin.check_permission('w', subject["profile"]["id"]):  # admin is allowed to delete the subject

            response = self.api.delete(f"/subject/{id_}")

            # display message that Subject has been deleted on the returned page.
            self.flash("Subject has been deleted")
            return redirect(url_for("subjects"))

        else:  # admin is not allowed to see subjects
            self.flash("You are not allowed to delete subjects. ")
            return redirect(url_for("subjects"))
