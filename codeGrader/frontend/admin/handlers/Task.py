# CodeGrader - https://github.com/ooemperor/CodeGrader
# Copyright © 2023, 2024 Michael Kaiser <michael.kaiser@emplabs.ch>
#
# This file is part of CodeGrader.
#
# CodeGrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CodeGrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CodeGrader.  If not, see <http://www.gnu.org/licenses/>.

"""
Handlers for the rendering of Task
@author: mkaiser
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from typing import Union


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

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get and render the page for a given task by its id
        @param id_: The id of the task
        @type id_: int
        @return: The rendered page of the task
        @rtype: HTML
        """
        task = self.api.get(f"/task/{id_}")

        editable = self.admin.check_permission('w', task["profile"]["id"])
        exercises = self.api.get("/exercises", profile=self.admin.get_filter_profile())
        submissions = self.api.get("/submissions", profile=self.admin.get_filter_profile(), task_id=id_)
        testcases = self.api.get("/testcases", task_id=id_)
        task["exercises"] = exercises["exercise"]
        if "submission" in submissions.keys():  # handles the case that there are no submissions yet
            task["submissions"] = submissions["submission"]

        if "testcase" in testcases.keys():  # handles the case that there are no submissions yet
            task["testcases"] = testcases["testcase"]

        task["editable"] = editable
        if self.admin.check_permission('r', task["profile"]["id"]):  # when admin is allowed to view this task
            print(task)
            return render_template("task.html", **task)

        else:  # admin is not allowed to view this task
            self.flash("You are not allowed to view this task. ")
            return redirect(url_for("tasks"))

    def post(self, id_: int) -> Response:
        """
        Handler for the update of a task
        @param id_: The identifier of the task
        @return:
        """
        assert self.request.form is not None

        task_before = self.api.get(f"/task/{id_}")  # get the task data
        if self.admin.check_permission('w', task_before["profile"]["id"]):
            task_data = dict()

            task_data["name"] = self.get_value("name")
            task_data["tag"] = self.get_value("tag")
            task_data["description"] = self.get_value("description")
            task_data["exercise_id"] = self.get_value("exercise")

            # getting the data from the form provided in the request
            self.api.put(f"/task/{id_}", body=task_data)

        else:  # admin is not allowed
            self.flash("You are not allowed to update this task")

        # either way redirect to the task
        return redirect(url_for("task", id_=id_))


class AddTaskHandler(BaseHandler):
    """
    Class to handle the operations of creating a task.
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the AddTask Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self) -> Union[str, Response]:
        """
        Render the template for adding
        @return: The rendered page
        """

        if self.admin.check_permission('w', 'task'):
            task = dict()
            exercises = self.api.get("/exercises", profile=self.admin.get_filter_profile())
            task["exercises"] = exercises["exercise"]
            print(task)
            return render_template("addTask.html", **task)

        else:  # admin is not allowed to view this task
            self.flash("You are not allowed to access this site! ")
            return redirect(url_for("tasks"))

    def post(self) -> Response:
        """
        Post Operation
        get the data out of the request and create the task in the backend via api
        @return: redirect to another page
        """
        if self.admin.check_permission('w', create_object='task'):
            task_data = dict()

            task_data["name"] = self.get_value("name")
            task_data["tag"] = self.get_value("tag")
            task_data["exercise_id"] = self.get_value("exercise")

            self.api.post("/task/add", body=task_data)

        else:
            self.flash("You are not allowed to view this site")

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

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get Handler to render the site for confirmation for deletion of a Task
        @param id_: The id_ of the task
        @type id_: int
        @return: Rendered Template
        """
        task = self.api.get(f"/task/{id_}")

        editable = self.admin.check_permission('w', task["profile"]["id"])

        if editable:
            return render_template("deleteTask.html", **task)

        else:
            self.flash("You are not allowed to delete tasks")
            return redirect(url_for("tasks"))

    def post(self, id_: int) -> Response:
        """
        Post Operation for Task Deletion
        Deletes the task in the backend via an API Call
        @param id_: The idnentifier of the Task
        @type id_: int
        @return: Redirection to the Task table
        """
        task = self.api.get(f"/task/{id_}")
        if self.admin.check_permission('w', task["profile"]["id"]):  # admin is allowed to delete the task

            response = self.api.delete(f"/task/{id_}")
            # display message that task has been deleted on the returned page.
            self.flash("Task has been deleted")
            return redirect(url_for("tasks"))

        else:  # admin is not allowed to delete tasks
            self.flash("You are not allowed to delete tasks. ")
            return redirect(url_for("tasks"))


