"""
Handler Classes for the Users
"""
import flask
import flask_login
from flask import request, render_template, redirect
from .Base import BaseHandler


class HomeHandler(BaseHandler):
    """
    Handles Operations for the Home site
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the Home Handler
        @param request: The request from the app route of flask
        @type request: flask.request
        """
        super().__init__(request)

    def get(self):
        return render_template("home.html")
