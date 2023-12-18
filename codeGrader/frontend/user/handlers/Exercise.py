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
        @return:
        """

        exercise = self.api.get(f"/exercise/{id_}")

        if self.user.check_permission(exercise["profile"]["id"]):  # when admin is allowed to view this user
            return render_template("exercise.html", **exercise)

        else:  # admin is not allowed to see exercise
            self.flash("You are not allowed to view this exercise. ")
            return redirect(url_for("exercises"))
