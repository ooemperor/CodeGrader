"""
Handler Classes for the Users
@author: mkaiser
"""
import flask
import json
from flask import request, render_template, redirect
from .Base import BaseHandler


class UsersHandler(BaseHandler):
    """
    Handles Operations for the Users site
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the Users Handler
        @param request: The request from the app route of flask
        @type request: flask.request
        """
        super().__init__(request)

    def get(self):
        """
        Renders the template for the Users site.
        @return: The rendered template
        @rtype: HTML
        """
        users = self.api.get("/users")
        print(users)
        return render_template("users.html", **users)
