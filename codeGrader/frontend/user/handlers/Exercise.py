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
Handler Class for the Exercise Objects
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from typing import Union


class ExerciseListHandler(BaseHandler):
    """
    Handler Class for the List of all Exercises visible to the user
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the ExercisesListHandler
        @param request: The flask Request received from the routes file
        @type request: flask.Request
        @return: Nothign
        @rtype: None
        """
        super().__init__(request)

    def get(self) -> str:
        """
        Renders the template for the exercises site
        @return: The rendered template
        """
        exercises = self.api.get("/exercises", profile=self.user.get_filter_profile())
        return render_template("exercises.html", **exercises, this=self)


class ExerciseHandler(BaseHandler):
    """
    Handler Class for a single Exercise
    """
    def __init__(self, request: flask.Request) -> None:
        """
        Constructor for the handler of a single Exercise
        @param request: The request provided by the routes file
        @type request: flask.Request
        @return: Nothing
        @rtype: None
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get Method to render or redirect for a specific Exercise
        @param id_: The identifier of the object
        @type id_: int
        @return: The rendered site or a redirect
        @rtype: str|Response
        """

        exercise = self.api.get(f"/exercise/{id_}")
        exercise_score_raw = self.api.get(f"/scores/exercise", user_id=self.user.id, object_id=exercise["id"])
        score = exercise_score_raw['exercise'][0][str(exercise['id'])][0]['score']
        exercise["score"] = score

        if self.user.check_permission(exercise["profile"]["id"]):  # when user is allowed to view this user
            return render_template("exercise.html", **exercise)

        else:  # admin is not allowed to see exercise
            self.flash("You are not allowed to view this exercise. ")
            return redirect(url_for("exercises"))
