"""
Handler Classes for the home site of the admin panel.
"""
import flask
import flask_login
from flask import request, render_template, redirect
from .Base import BaseHandler


class HomeHandler(BaseHandler):
    """
    Handles Operations for the Home site
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the Home Handler
        @param request: The request from the app route of flask
        @type request: flask.request
        """
        super().__init__(request)

    def get(self) -> str:
        """
        Render the homeplate and return it
        @return: The rendered site
        @rtype: str
        """
        return render_template("home.html")
