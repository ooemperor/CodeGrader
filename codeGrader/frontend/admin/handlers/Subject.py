"""
Handlers for the rendering of Subjects
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for, flash
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

        self.api.post("/subject/add", body=subject_data)

        return redirect(url_for("subjects"))


class DeleteSubjectHandler(BaseHandler):
    """
    Handler to delete a Subject from the api backend
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the DeleteSubjectHandler Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int):
        """
        Get Handler to render the site for confirmation for deletion of a Subject
        @param id_: The id_ of the Subject
        @type id_: int
        @return: Rendered Template
        """
        subject = self.api.get(f"/subject/{id_}")

        return render_template("deleteSubject.html", **subject)

    def post(self, id_: int):
        """
        Post Operation for Subject Deletion
        Deletes the subject in the backend via an API Call
        @param id_: The idnentifier of the Subject
        @type id_: int
        @return: Redirection to the Subject table
        """
        if self.get_value("action_button") == "Submit":
            response = self.api.delete(f"/subject/{id_}")

            # display message that Subject has been deleted on the returned page.
            flash("Subject has been deleted")
            return redirect(url_for("subjects"))

        elif self.get_value("action_button") == "Cancel":
            return redirect(url_for("subject", id_=id_))

        else:
            pass
            # TODO Implement Error
