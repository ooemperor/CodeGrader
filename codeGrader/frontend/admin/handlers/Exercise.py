"""
Handlers for the rendering of exercise
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from typing import Union


class ExerciseListHandler(BaseHandler):
    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the exerciseListHandler
        Will Render the HTML Template for all the exercises.
        """
        super().__init__(request)

    def get(self) -> str:
        """
        Renders the template for the exercises site.
        @return: The rendered template
        @rtype: HTML
        """
        exercises = self.api.get("/exercises", profile=self.admin.get_filter_profile())
        return render_template("exercises.html", **exercises, this=self)


class ExerciseHandler(BaseHandler):
    """
    Handles the operation on a single exercise
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the exercise Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get and render the page for a given exercise by its id
        @param id_: The id of the exercise
        @type id_: int
        @return: The rendered page of the exercise
        @rtype: HTML
        """
        exercise = self.api.get(f"/exercise/{id_}")

        editable = self.admin.check_permission('w', exercise["profile"]["id"])
        subjects = self.api.get("/subjects", profile=self.admin.get_filter_profile())

        exercise["subjects"] = subjects["subject"]

        exercise["editable"] = editable

        if self.admin.check_permission('r', exercise["profile"]["id"]):  # when admin is allowed to view this user
            return render_template("exercise.html", **exercise)

        else:  # admin is not allowed to see exercise
            self.flash("You are not allowed to view this exercise. ")
            return redirect(url_for("exercises"))

    def post(self, id_: int) -> Response:
        """
        Handler for the update of an exercise
        @param id_: The identifier of the exercise
        @return:
        """
        assert self.request.form is not None

        exercise_before = self.api.get(f"/exercise/{id_}")  # get the exercise data
        if self.admin.check_permission('w', exercise_before["profile"]["id"]):
            exercise_data = dict()

            exercise_data["name"] = self.get_value("name")
            exercise_data["tag"] = self.get_value("tag")

            exercise_data["subject_id"] = self.get_value("subject")

            # getting the data from the form provided in the request
            self.api.put(f"/exercise/{id_}", body=exercise_data)

        else:  # admin is not allowed to update
            self.flash("You are not allowed to update this exercise! ")

        # either way redirect to the exercise
        return redirect(url_for("exercise", id_=id_))


class AddExerciseHandler(BaseHandler):
    """
    Class to handle the operations of creating a exercise.
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the addExercise Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self) -> Union[str, Response]:
        """
        Render the template for adding
        @return: The rendered page
        """

        if self.admin.check_permission('w', 'exercise'):
            exercise_data = dict()
            subjects = self.api.get("/subjects", profile=self.admin.get_filter_profile())
            exercise_data["subjects"] = subjects["subject"]

            return render_template("addExercise.html", **exercise_data)

        else:  # admin is not allowed to view this exercise
            self.flash("You are not allowed to access this site! ")
            return redirect(url_for("exercises"))

    def post(self) -> Response:
        """
        Post Operation
        get the data out of the request and create the exercise in the backend via api
        @return: redirect to another page
        """
        assert self.request.form is not None

        if self.admin.check_permission('w', create_object='exercise'):
            exercise_data = dict()

            exercise_data["name"] = self.get_value("name")
            exercise_data["tag"] = self.get_value("tag")

            exercise_data["subject_id"] = self.get_value("subject")

            self.api.post("/exercise/add", body=exercise_data)

            return redirect(url_for("exercises"))


class DeleteExerciseHandler(BaseHandler):
    """
    Handler to delete a Exercise from the api backend
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the DeleteExerciseHandler Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get Handler to render the site for confirmation for deletion of a Exercise
        @param id_: The id_ of the Exercise
        @type id_: int
        @return: Rendered Template
        """
        exercise = self.api.get(f"/exercise/{id_}")

        editable = self.admin.check_permission('w', exercise["profile"]["id"])

        if editable:
            return render_template("deleteExercise.html", **exercise)

        else:
            self.flash("You are not allowed to delete Exercises")
            return redirect(url_for("exercises"))

    def post(self, id_: int) -> Response:
        """
        Post Operation for Exercise Deletion
        Deletes the exercise in the backend via an API Call
        @param id_: The idnentifier of the Exercise
        @type id_: int
        @return: Redirection to the Exercise table
        """
        exercise = self.api.get(f"/exercise/{id_}")
        if self.admin.check_permission('w', exercise["profile"]["id"]):  # admin is allowed to delete the exercise
            if self.get_value("action_button") == "Submit":

                response = self.api.delete(f"/exercise/{id_}")

                # display message that exercise has been deleted on the returned page.
                self.flash("Exercise has been deleted")
                return redirect(url_for("exercises"))

            elif self.get_value("action_button") == "Cancel":
                return redirect(url_for("exercise", id_=id_))

            else:
                pass
                # TODO Implement Error

        else:  # admin is not allowed to delete exercises
            self.flash("You are not allowed to delete exercises. ")
            return redirect(url_for("exercises"))
