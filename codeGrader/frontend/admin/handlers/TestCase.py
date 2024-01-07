"""
File for the Handlers for Testcase
@author: mkaiser
"""

import flask
import requests
from flask import request, render_template, redirect, url_for, flash, Response, send_file, stream_with_context
from .Base import BaseHandler
from typing import Union
import io


class AddTestCaseHandler(BaseHandler):
    """
    Class to handle adding of a TestCase to a Task
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the AddTestCaseHandler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, task_id) -> Union[str, Response]:
        """
        Render the template for creating and adding a testcase to a Task.
        @param task_id:
        @return: The rendered HTML Template
        @rtype: str
        """
        task = self.api.get(f"/task/{task_id}")
        editable = self.admin.check_permission('w', task["profile"]["id"])
        testcase = dict()
        testcase["task"] = task

        if editable:  # when admin is allowed to edit this testcase
            return render_template("addTestcase.html", **testcase)

        else:  # admin is not allowed to edit this testcase
            self.flash("You are not allowed to add Testcases. ")
            return redirect(url_for("task", id_=task_id))

    def post(self, task_id) -> Union[str, Response]:
        """
        Create the testcase in the backend and link it to the task.
        @param task_id: The id of the task, that the testcase shall be linked to
        @type task_id: int
        @return: Redirect to the on success or display an error message.
        @rtype: str or Response
        """
        assert self.request.form is not None
        assert self.request.files is not None
        assert len(
            self.request.files) == 2  # this will be true, even if one file has not been provided. (Mainpulation Check)
        assert "input_file" in self.request.files.keys()
        assert "output_file" in self.request.files.keys()
        task = self.api.get(f"/task/{task_id}")  # get the task data

        input_file_id = None
        output_file_id = None

        if self.admin.check_permission('w', task["profile"]["id"]):

            for file_key in self.request.files.keys():
                file = self.request.files[file_key]

                # upload the files to the backend api
                files = {file.filename: file}
                # constructing the url of the api call
                url = f"/file/upload"
                resp = self.api.post(url, files=files)  # uploading the file and retreiving response body

                if file_key == "input_file":
                    input_file_id = resp["response"]["id"]

                elif file_key == "output_file":
                    output_file_id = resp["response"]["id"]

                else:
                    raise NameError("The provided File id is not valid. Please Check with your administrator!")

            testcase_data = dict()

            testcase_data["task_id"] = task_id
            testcase_data["input_id"] = input_file_id
            testcase_data["output_id"] = output_file_id

            # getting the data from the form provided in the request
            self.api.post(f"/testcase/add", body=testcase_data)

        else:  # admin is not allowed to access
            self.flash("You are not allowed to add Testcases")

        # either way redirect to the task
        return redirect(url_for("task", id_=task_id))


class DeleteTestCaseHandler(BaseHandler):
    """
    Class for Handling the deletion of a TestCase
    """
    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the Handler of the TestCaseDeletionHandler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, testcase_id: int) -> Union[str, Response]:
        """
        Render the template for a testcase deletion if allowed.
        If the admin user is not allowed to see this, we redirect with an error message.
        @param id_: The id of the testcase in the database
        @type id_: int
        @return: The rendered HTML Template
        @rtype: str
        """
        testcase = self.api.get(f"/testcase/{testcase_id}")
        editable = self.admin.check_permission('w', testcase["task"]["profile"]["id"])

        if editable:  # when admin is allowed to edit this testcase
            return render_template("deleteTestCase.html", **testcase)

        else:
            self.flash("You are not allowed to delete this Testcase!")
            return url_for("task", id_= testcase["task"]["id"])

    def post(self, testcase_id) -> Union[str, Response]:
        """
        Create the testcase in the backend and link it to the task.
        @param task_id: The id of the task, that the testcase shall be linked to
        @type task_id: int
        @return: Redirect to the on success or display an error message.
        @rtype: str or Response
        """

        testcase = self.api.get(f"/testcase/{testcase_id}")
        editable = self.admin.check_permission('w', testcase["task"]["profile"]["id"])

        if editable:  # when admin is allowed to edit this testcase
            self.api.delete(f"/testcase/{testcase_id}")
            self.flash(f"Testcase {testcase_id} has been deleted!")

        else:
            self.flash("You are not allowed to delete this Testcase!")

        return redirect(url_for("task", id_=testcase["task"]["id"]))  # anyway we redirect to this site.


class TestCaseFileHandler(BaseHandler):
    """
    Handles the download (GET) Operation on a TestCaseFile
    This class will be inherited by the Input and OutputFileClass
    """
    file_type_name: str

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the TestCaseFileHandler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get and render the page for a given TestCaseFile by its id
        @param id_: The id of the TestCase
        @type id_: int
        @return: The File as a download
        @rtype: html
        """
        testcase = self.api.get(f"/testcase/{id_}")
        task_profile_id = testcase["task"]["profile"]["id"]
        task_id = testcase["task"]["profile"]["id"]

        if self.admin.check_permission('r', task_profile_id):  # when admin is allowed to view this File
            input_file_id = testcase["input_file_id"]

            req = self.api.get_file(f"/file/{input_file_id}")
            filename = testcase[self.file_type_name]["filename"]
            req.headers['Content-Disposition'] = f"attachment;filename={filename}"
            return Response(stream_with_context(req.iter_content(chunk_size=2048)),
                            content_type=req.headers["content-type"])

        else:  # admin is not allowed to view this testcase
            self.flash("You are not allowed to download this file. ")
            return redirect(url_for("task", id_=task_id))


class TestCaseInputFileHandler(TestCaseFileHandler):
    """
    Handles the download (GET) Operation on a TestCaseInputFile
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the TestCaseInputFileHandler Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)
        self.file_id_name = "input_file_id"
        self.file_type_name = "input_file"


class TestCaseOutputFileHandler(TestCaseFileHandler):
    """
    Handles the download (GET) Operation on a TestCaseOutputFile
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the TestCaseOutputFileHandler Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)
        self.file_id_name = "output_file_id"
        self.file_type_name = "output_file"
