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
Handler Class for the Subject Objects
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from typing import Union


class SubjectListHandler(BaseHandler):
    """
    Handler Class for the List of all Subjects visible to the user
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the SubjectsListHandler
        @param request: The flask Request received from the routes file
        @type request: flask.Request
        @return: Nothign
        @rtype: None
        """
        super().__init__(request)

    def get(self) -> str:
        """
        Renders the template for the subjects site
        @return: The rendered template
        """
        subjects = self.api.get("/subjects")


        for sub in subjects["subject"]:
            # filtering only the subjects that are allowed by the memberships
            if not self.user.check_permission(subject_id=sub["id"]):
                subjects["subject"].remove(sub)

        return render_template("subjects.html", **subjects, this=self)


class SubjectHandler(BaseHandler):
    """
    Handler Class for a single Subject
    """
    def __init__(self, request: flask.Request) -> None:
        """
        Constructor for the handler of a single Subject
        @param request: The request provided by the routes file
        @type request: flask.Request
        @return: Nothing
        @rtype: None
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get Method to render or redirect for a specific Subject
        @param id_: The identifier of the object
        @type id_: int
        @return: The rendered site or a redirect
        @rtype: str|Response
        """

        subject = self.api.get(f"/subject/{id_}")
        subject_score_raw = self.api.get(f"/scores/subject", user_id=self.user.id, object_id=subject["id"])
        score = subject_score_raw['subject'][0][str(subject['id'])][0]['score']
        subject["score"] = score

        if self.user.check_permission(subject_id = subject["id"]):  # when user is allowed to view this subject
            return render_template("subject.html", **subject)

        else:  # admin is not allowed to see subject
            self.flash("You are not allowed to view this subject. ")
            return redirect(url_for("subjects"))
