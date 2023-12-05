"""
Handlers for the rendering of Task
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler


class TaskListHandler(BaseHandler):
    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the TaskListHandler
        Will Render the HTML Template for all the tasks.
        """
        super().__init__(request)

    def get(self) -> str:
        """
        Renders the template for the tasks site.
        @return: The rendered template
        @rtype: HTML
        """
        tasks = self.api.get("/tasks", profile=self.admin.get_filter_profile())
        return render_template("tasks.html", **tasks, this=self)


class TaskHandler(BaseHandler):
    """
    Handles the operation on a single task
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the task Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> str:
        """
        Get and render the page for a given task by its id
        @param id_: The id of the task
        @type id_: int
        @return: The rendered page of the task
        @rtype: HTML
        """
        task = self.api.get(f"/task/{id_}")
        return render_template("task.html", **task)

    def post(self, id_: int) -> Response:
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


class AddTaskHandler(BaseHandler):
    """
    Class to handle the operations of creating a user.
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the AddTask Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self) -> str:
        """
        Render the template for adding
        @return: The rendered page
        """

        return render_template("addTask.html")

    def post(self) -> Response:
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


class DeleteTaskHandler(BaseHandler):
    """
    Handler to delete a Task from the api backend
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the DeleteTaskHandler Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> str:
        """
        Get Handler to render the site for confirmation for deletion of a Task
        @param id_: The id_ of the user
        @type id_: int
        @return: Rendered Template
        """
        task = self.api.get(f"/task/{id_}")

        return render_template("deleteTask.html", **task)

    def post(self, id_: int) -> Response:
        """
        Post Operation for Task Deletion
        Deletes the task in the backend via an API Call
        @param id_: The idnentifier of the Task
        @type id_: int
        @return: Redirection to the Task table
        """
        if self.get_value("action_button") == "Submit":
            response = self.api.delete(f"/task/{id_}")

            # display message that task has been deleted on the returned page.
            self.flash("Task has been deleted")
            return redirect(url_for("tasks"))

        elif self.get_value("action_button") == "Cancel":
            return redirect(url_for("task", id_=id_))

        else:
            pass
            # TODO Implement Error
