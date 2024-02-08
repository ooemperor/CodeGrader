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
Handler Class for the Submission for a given task.
"""

import flask
from flask import request, render_template, redirect, url_for, flash, Response
from .Base import BaseHandler
from typing import Union


class SubmissionHandler(BaseHandler):
    """
    Class to handle the Requests for a submission
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the Handler
        """
        super().__init__(request)

    def get_gamification(self, id_: int) -> str:
        """
        Render for the submission result
        @param id_: The identifier of the submission
        @type id_: int
        @return: HTML Code that will be inserted into the rendered html via javascript /
        This html code is only a snippet and not complete code
        """
        if id_ == 0:
            return ""  # we do not return anything

        else:
            # we need to prepare the data now
            submission = self.api.get(f"/submission/{id_}")
            state = submission["state"]
            score = float(submission["max_score"])

            if state != "finished":
                return '<img src="https://media.tenor.com/aXbaXzhcVVUAAAAM/hi.gif" alt="Hi GIF - Hi GIFs" loading="lazy" style="background-color: unset;" width="158" height="127.11818181818181">'

            else:
                # submission has finished in the backend, need to calculate the result base on the score.
                if score == 100.0:
                    return '<img src="https://media1.tenor.com/m/oMnCJU2dp5oAAAAd/one-hundred-percent-sophie.gif" width="833" height="833" alt="One Hundred Percent Sophie GIF - One Hundred Percent Sophie How I Met Your Father GIFs" style="max-width: 833px;">'

                elif score == 0.0:
                    return '<img src="https://media1.tenor.com/m/1dvdDJ0TumUAAAAC/thisisfine-disaster.gif" width="833" height="468.5625" alt="Thisisfine Disaster GIF - Thisisfine Disaster Denial GIFs" style="max-width: 833px; background-color: rgb(174, 153, 71);">'

                else:
                    return '<img src="https://media1.tenor.com/m/DgPnCr2BbOcAAAAd/not-good-not-bad-not-good.gif" width="833" height="786.14375" alt="Not Good Not Bad Good And Bad GIF - Not Good Not Bad Not Good Not Bad GIFs" style="max-width: 833px;">'


class AddSubmissionHandler(BaseHandler):
    """
    Class to handle the upload of an submission
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the Handler
        """
        super().__init__(request)

    def post(self, id_: int) -> Response:
        """
        Handler for adding a Submission to a task for a user
        @param id_: The identifier of the task
        @type id_: int
        @return: A redirect to another site
        @rtype: Response
        """
        assert self.request.form is not None
        assert self.request.files is not None

        user_id = self.user.id
        task_id = id_

        submission_id = None

        for file_key in self.request.files.keys():
            file = self.request.files[file_key]

            # upload the files to the backend api
            files = {file.filename: file}
            # constructing the url of the api call
            url = f"/file/upload"
            resp = self.api.post(url, files=files)  # uploading the file and retreiving response body

            file_id = resp["response"]["id"]
            body = ({"task_id": task_id, "file_id": file_id, "user_id": user_id})
            url = f"/submission/add"

            response = self.api.post(url, body=body)  # adding the submission via file_id
            print(response)
            submission_id = response["response"]["id"]


        # either way redirect to the task
        self.flash(f"Submission received with id_ {submission_id}")
        return redirect(url_for("task", id_=id_, submission_id=submission_id))
