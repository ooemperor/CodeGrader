"""
Handlers for the rendering of Task
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for
from .Base import BaseHandler


class TaskListHandler(BaseHandler):
    def __init(self, request: flask.Request):
        """
        Constructor of the TaskListHandler
        Will Render the HTML Template for all the tasks.
        """
        super().__init__(request)

    def get(self):
        """
        Renders the template for the tasks site.
        @return: The rendered template
        @rtype: HTML
        """
        tasks = self.api.get("/tasks")
        return render_template("tasks.html", **tasks)


class TaskHandler(BaseHandler):
    """
    Handles the operation on a single task
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the task Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int):
        """
        Get and render the page for a given task by its id
        @param id_: The id of the task
        @type id_: int
        @return: The rendered page of the task
        @rtype: HTML
        """
        task = self.api.get(f"/task/{id_}")
        return render_template("task.html", **task)

    def post(self, id_: int):
        """
        Handler for the update of a task
        @param id_: The identifier of the task
        @return:
        """
        assert self.request.form is not None
        task_data = dict()

        task_data["name"] = self.get_value("name")
        task_data["tag"] = self.get_value("tag")

        # getting the data from the form provided in the request
        self.api.put(f"/task/{id_}", body=task_data)

        return redirect(url_for("task", id_=id_))
