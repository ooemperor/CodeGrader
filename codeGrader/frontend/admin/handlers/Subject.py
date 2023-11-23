"""
Handlers for the rendering of Subjects
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for
from .Base import BaseHandler


class SubjectListHandler(BaseHandler):
    def __init(self, request: flask.Request):
        """
        Constructor of the SubjectListHandler
        Will Render the HTML Template for all the subjects.
        """
        super().__init__(request)

    def get(self):
        """
        Renders the template for the Subjects site.
        @return: The rendered template
        @rtype: HTML
        """
        subjects = self.api.get("/subjects")
        return render_template("subjects.html", **subjects)


class SubjectHandler(BaseHandler):
    """
    Handles the operation on a single Subject
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the Subject Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int):
        """
        Get and render the page for a given subject by its id
        @param id_: The id of the subject
        @type id_: int
        @return: The rendered page of the subject
        @rtype: HTML
        """
        subject = self.api.get(f"/subject/{id_}")
        return render_template("subject.html", **subject)

    def post(self, id_: int):
        """
        Handler for the update of a subject
        @param id_: The identifier of the subject
        @return:
        """
        assert self.request.form is not None
        subject_data = dict()

        subject_data["name"] = self.get_value("name")
        subject_data["tag"] = self.get_value("tag")

        # getting the data from the form provided in the request
        self.api.put(f"/subject/{id_}", body=subject_data)

        return redirect(url_for("subject", id_=id_))


class AddSubjectHandler(BaseHandler):
    """
    Class to handle the operations of creating a user.
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the AddSubject Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self):
        """
        Render the template for adding
        @return: The rendered page
        """

        return render_template("addSubject.html")

    def post(self):
        """
        Post Operation
        get the data out of the request and create the subject in the backend via api
        @return: redirect to another page
        """

        subject_data = dict()

        subject_data["name"] = self.get_value("name")
        subject_data["tag"] = self.get_value("tag")

        self.api.post("/addSubject", body=subject_data)

        return redirect("subjects")
