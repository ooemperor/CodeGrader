"""
Handlers for the rendering of exercise
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for
from .Base import BaseHandler


class ExerciseListHandler(BaseHandler):
    def __init(self, request: flask.Request):
        """
        Constructor of the exerciseListHandler
        Will Render the HTML Template for all the exercises.
        """
        super().__init__(request)

    def get(self):
        """
        Renders the template for the exercises site.
        @return: The rendered template
        @rtype: HTML
        """
        exercises = self.api.get("/exercises")
        return render_template("exercises.html", **exercises)


class ExerciseHandler(BaseHandler):
    """
    Handles the operation on a single exercise
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the exercise Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int):
        """
        Get and render the page for a given exercise by its id
        @param id_: The id of the exercise
        @type id_: int
        @return: The rendered page of the exercise
        @rtype: HTML
        """
        exercise = self.api.get(f"/exercise/{id_}")
        return render_template("exercise.html", **exercise)

    def post(self, id_: int):
        """
        Handler for the update of an exercise
        @param id_: The identifier of the exercise
        @return:
        """
        assert self.request.form is not None
        exercise_data = dict()

        exercise_data["name"] = self.get_value("name")
        exercise_data["tag"] = self.get_value("tag")

        # getting the data from the form provided in the request
        self.api.put(f"/exercise/{id_}", body=exercise_data)

        return redirect(url_for("exercise", id_=id_))
