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
Handler Class for the Task
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from typing import Union


class TaskListHandler(BaseHandler):
    """
    Handler for the List of Tasks
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the TaskListHandler
        @param request: The flask Request received from the routes file
        @type request: flask.Request
        @return: Nothing
        @rtype: None
        """
        super().__init__(request)

    def get(self) -> str:
        """
        Renders the template for the tasks site
        @return: The rendered template
        """
        tasks = self.api.get("/tasks", profile=self.user.get_filter_profile())
        return render_template("tasks.html", **tasks, this=self)


class TaskHandler(BaseHandler):
    """
    Handler Class for a single Task
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor for the handler of a single Task
        @param request: The request provided by the routes file
        @type request: flask.Request
        @return: Nothing
        @rtype: None
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get Method to render or redirect for a specific Task
        @param id_: The identifier of the object
        @type id_: int
        @return:
        """

        task = self.api.get(f"/task/{id_}")

        if self.user.check_permission(task["profile"]["id"]):  # when admin is allowed to view this user
            submissions = self.api.get(f"/submissions", task_id=id_, user_id=self.user.id)
            if "submission" in submissions.keys():  # handles the case that there are no submissions yet
                task["submissions"] = submissions["submission"]
            return render_template("task.html", **task)

        else:  # admin is not allowed to see exercise
            self.flash("You are not allowed to view this task. ")
            return redirect(url_for("tasks"))
