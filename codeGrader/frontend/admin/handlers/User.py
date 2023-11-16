"""
Handler Classes for the Users
@author: mkaiser
"""
import flask
import json
from flask import request, render_template, redirect
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
        print(user)
        return render_template("user.html", **user)
