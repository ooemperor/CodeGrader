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

    def create(self):
        """
        Create a User in the database
        @return:
        """
        user_data = dict()

        user_data["username"] = self.get_value("username")
        user_data["first_name"] = self.get_value("first_name")
        user_data["last_name"] = self.get_value("last_name")
        user_data["email"] = self.get_value("email")
        user_data["tag"] = self.get_value("tag")
        user_data["profile"] = self.get_value("profile")

        response_text = self.api.post("/addUser", body=user_data)

        id_ = response_text["response"]["id"]

        return redirect(url_for("user", id_=id_))


class AddTaskHandler(BaseHandler):
    """
    Class to handle the operations of creating a user.
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the AddTask Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self):
        """
        Render the template for adding
        @return: The rendered page
        """

        return render_template("addTask.html")

    def post(self):
        """
        Post Operation
        get the data out of the request and create the task in the backend via api
        @return: redirect to another page
        """

        task_data = dict()

        task_data["name"] = self.get_value("name")
        task_data["tag"] = self.get_value("tag")

        self.api.post("/task/add", body=task_data)

        return redirect(url_for("tasks"))
