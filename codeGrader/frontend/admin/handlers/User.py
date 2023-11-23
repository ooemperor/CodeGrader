"""
Handler Classes for the Users in the admin frontend
@author: mkaiser
"""
import flask
import json
from flask import request, render_template, redirect, url_for
from .Base import BaseHandler


class UserListHandler(BaseHandler):
    """
    Handles Operations for the Users site
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the Users Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self):
        """
        Renders the template for the Users site.
        @return: The rendered template
        @rtype: HTML
        """
        users = self.api.get("/users")
        return render_template("users.html", **users)


class UserHandler(BaseHandler):
    """
    Handles the operation on a single User
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the User Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int):
        """
        Get and render the page for a given user by its id
        @param id_: The id of the user
        @type id_: int
        @return: The rendered page of the user
        @rtype: HTML
        """
        user = self.api.get(f"/user/{id_}")
        profiles = self.api.get(f"/profiles")
        user["profiles"] = profiles["profile"]
        return render_template("user.html", **user)

    def post(self, id_: int):
        """
        Handler for the update of a user
        @param id_:
        @param data:
        @return:
        """
        assert self.request.form is not None
        user_data = dict()

        # getting the data from the form provided in the request
        user_data["username"] = self.get_value("username")
        user_data["first_name"] = self.get_value("first_name")
        user_data["last_name"] = self.get_value("last_name")
        user_data["email"] = self.get_value("email")
        user_data["tag"] = self.get_value("tag")

        user_data["profile_id"] = self.get_value("profile")

        self.api.put(f"/user/{id_}", body=user_data)

        return redirect(url_for("user", id_=id_))


class AddUserHandler(BaseHandler):
    """
    Handler Class for the creation of an user
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the AddAdminUser Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self):
        """
        Get and render the site to create an admin user
        @return: The rendered page.
        """
        user_data = dict()

        profiles = self.api.get(f"/profiles")
        user_data["profiles"] = profiles["profile"]

        return render_template("addUser.html", **user_data)

    def post(self):
        """
        Post Operation
        Creates the admin user specified by the parameters in the backend.
        @return: Redirect to the adminUsers Site
        """
        assert self.request.form is not None
        user_data = dict()

        # getting the data from the form provided in the request
        user_data["username"] = self.get_value("username")
        user_data["first_name"] = self.get_value("first_name")
        user_data["last_name"] = self.get_value("last_name")
        user_data["email"] = self.get_value("email")
        user_data["tag"] = self.get_value("tag")
        user_data["password"] = self.get_value("password")

        user_data["profile_id"] = self.get_value("profile")

        self.api.post(f"/user/add", body=user_data)

        return redirect(url_for("users"))
