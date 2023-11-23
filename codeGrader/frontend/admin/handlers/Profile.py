"""
Handlers for the rendering of profiles
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for
from .Base import BaseHandler


class ProfileListHandler(BaseHandler):
    def __init(self, request: flask.Request):
        """
        Constructor of the ProfileListHandler
        Will Render the HTML Template for all the profiles.
        """
        super().__init__(request)

    def get(self):
        """
        Renders the template for the Profiles site.
        @return: The rendered template
        @rtype: HTML
        """
        profiles = self.api.get("/profiles")
        return render_template("profiles.html", **profiles)


class ProfileHandler(BaseHandler):
    """
    Handles the operation on a single Profile
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the Profile Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int):
        """
        Get and render the page for a given profile by its id
        @param id_: The id of the profile
        @type id_: int
        @return: The rendered page of the profile
        @rtype: HTML
        """
        profile = self.api.get(f"/profile/{id_}")
        return render_template("profile.html", **profile)

    def post(self, id_: int):
        """
        Handler for the update of a Profile
        @param id_: The identifier of the profile
        @return:
        """
        assert self.request.form is not None
        profile_data = dict()

        profile_data["name"] = self.get_value("name")
        profile_data["tag"] = self.get_value("tag")

        # getting the data from the form provided in the request
        self.api.put(f"/profile/{id_}", body=profile_data)

        return redirect(url_for("profile", id_=id_))


class AddProfileHandler(BaseHandler):
    """
    Class to handle the operations of creating a user.
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the AddProfile Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self):
        """
        Render the template for adding
        @return: The rendered page
        """

        return render_template("addProfile.html")

    def post(self):
        """
        Post Operation
        get the data out of the request and create the profile in the backend via api
        @return: redirect to another page
        """

        profile_data = dict()

        profile_data["name"] = self.get("name")
        profile_data["tag"] = self.get_value("tag")

        self.api.post("/addProfile", body=profile_data)

        return redirect("profiles")
