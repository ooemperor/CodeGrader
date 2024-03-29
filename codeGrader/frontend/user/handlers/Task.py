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
from flask import request, render_template, redirect, url_for, flash, Response, Request
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
        tasks = self.api.get("/tasks")
        temp_tasks = tasks["task"].copy()
        for t in temp_tasks:
            # filtering only the tasks that are allowed by the memberships
            if not self.user.check_permission(subject_id = t["subject_id"]):
                tasks["task"].remove(t)

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

    def get(self, id_: int, arguments: Request.args) -> Union[str, Response]:
        """
        Get Method to render or redirect for a specific Task
        @param id_: The identifier of the object
        @type id_: int
        @param arguments:  The arguments passed to the function in the url /
        This is used when we want to live render the execution of the submission
        @rtype: int
        @return:
        """

        task = self.api.get(f"/task/{id_}")

        if "submission_id" in arguments.keys():
            task["submission_id"] = arguments["submission_id"]

        else:
            task["submission_id"] = 0

        if self.user.check_permission(subject_id=task["subject_id"]):  # when user is allowed to view this task
            submissions = self.api.get(f"/submissions", task_id=id_, user_id=self.user.id)
            if "submission" in submissions.keys():  # handles the case that there are no submissions yet
                task["submissions"] = submissions["submission"]

                # calculating the maximal score of the user
                max_score = 0
                for sub in submissions["submission"]:
                    # finding the max score and updating the variable if new high score is found
                    temp_score = sub["max_score"]
                    if temp_score is None:
                        continue

                    elif int(temp_score) > max_score:
                        max_score = int(temp_score)
                    else:
                        continue

                task["max_score"] = max_score

            return render_template("task.html", **task)

        else:  # admin is not allowed to see exercise
            self.flash("You are not allowed to view this task. ")
            return redirect(url_for("tasks"))
