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
Route definition and main File that runs the application.
@author: mkaiser
@version: 1.0
"""
import io
import mimetypes
import json
import urllib
from functools import wraps
from gevent.pywsgi import WSGIServer

from flask import Flask, request, send_file
from flask_caching import Cache
from codeGrader.backend.config import config
from codeGrader.backend.api.handlers import UserHandler, ProfileHandler, AdminUserHandler, SubjectHandler, \
    ExerciseHandler, TaskHandler, FileHandler, SubmissionHandler, TestCaseHandler, AdminUserLoginHandler, \
    authentication, AdminTypeHandler, UserLoginHandler, InstructionHandler, AttachmentHandler, ScoreHandler, \
    AdminUserPasswordResetHandler, UserPasswordResetHandler, MembershipHandler
from codeGrader.backend.api.logger import Logger
from codeGrader.backend.api.util import upload_file, preprocess_task_file
import logging
import datetime

# construction of Application and DB Connection
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
app = Flask(config.appName)
cache.init_app(app)
cache.memoize()

# disabling the integrated logger if set so in the config. 
if not config.useIntegratedLogin:
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True

# adding the custom logger
log = Logger()


def app_index():
    """
    Calculates a JSON dict with the representaion of all the Routes in this application
    @return: The routes as a JSON representation
    @rtype: dict
    """
    output = dict()
    output_data = []
    for route in app.url_map.iter_rules():
        method = route.methods
        rule = route.rule
        endpoint = route.endpoint
        output_data.append({rule: {"methods": method, "endpoint": endpoint}})
    output["routes"] = output_data
    return output


def cache_bypass(*args, **kwargs):
    """
    Callable function to check if the cache should be bypassed or not.
    @param args: Optional arguments as list
    @param kwargs: Key-Value Pair of optional values
    @return: True if the cache shall not be used, else False. False means, that we will use the caching values.
    """
    if config.cache_bypass is True:
        return True  # cache will not be used
    elif request.method == 'GET':
        return False  # cached willl be used and will not be bypassed
    else:
        return True  # cache will not be used


@app.route("/", methods=['POST', 'GET'])
@cache.memoize(60, unless=cache_bypass)
@authentication
def home() -> dict:
    """
    Returns the answer to all questions
    @return: The answer to all the questions
    """
    response = {"response": "42"}
    return response


@app.route("/index", methods=['GET'])
@cache.memoize(config.cache_timeout, unless=cache_bypass)
@authentication
def index() -> dict:
    """
    Returns the calculated index of all the routes in this application
    @return: Returns the calculated index of all the routes in this application
    @rtype: dict
    """
    return app_index()


@app.route("/admin/login", methods=['POST'])
@authentication
def admin_login() -> dict:
    """
    Login for a provided Admin User
    """
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    return AdminUserLoginHandler().login(username, password)


@app.route("/user/login", methods=['POST'])
@authentication
def user_login() -> dict:
    """
    Login for a provided user
    """
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    return UserLoginHandler().login(username, password)


@app.route("/user/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
@cache.memoize(config.cache_timeout, unless=cache_bypass)
@authentication
def user(id_: int) -> dict:
    """
    Route for get, post, put of user elements.
    @param id_: The identifier of the user
    @type id_: int
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'GET':
        return UserHandler().get(id_)

    elif request.method == 'PUT':
        cache.clear()
        return UserHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        cache.clear()
        return UserHandler().delete(id_)


@app.route("/user/<int:id_>/password/reset", methods=['POST'])
@authentication
def user_password_reset(id_: int) -> dict:
    """
    Route for password reset on a user
    @param id_: The identifier of the user
    @type id_: int
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'POST':
        return UserPasswordResetHandler().reset(id_)


@app.route("/user/<int:id_>/password/update", methods=['POST'])
@authentication
def user_password_update(id_: int) -> dict:
    """
    Route for password reset on a admin user
    @param id_: The identifier of the admin user
    @type id_: int
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'POST':
        user_id = request.get_json()["id"]
        password = request.get_json()["password"]
        return UserPasswordResetHandler().change(id_, password)


@app.route("/users", methods=['GET'])
@cache.cached(config.cache_timeout, unless=cache_bypass, query_string=True)
@authentication
def users() -> dict:
    """
    Getting all the users objects out of the database
    @return: Custom Representation of all the user objects
    @rtype: dict
    """
    return UserHandler().get_all(request.args)


@app.route("/user/add", methods=['POST'])
@authentication
def addUser() -> dict:
    """
    Adding a new user in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    cache.clear()
    return UserHandler().post(request.get_json())


@app.route("/admin/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
@cache.memoize(config.cache_timeout, unless=cache_bypass)
@authentication
def admin(id_: int) -> dict:
    """
    Route for get, post, put of user elements.
    @param id_: The identifier of the user
    @type id_: int
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'GET':
        return AdminUserHandler().get(id_)

    elif request.method == 'PUT':
        cache.clear()
        return AdminUserHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        cache.clear()
        return AdminUserHandler().delete(id_)


@app.route("/admin/<int:id_>/password/reset", methods=['POST'])
@authentication
def admin_password_reset(id_: int) -> dict:
    """
    Route for password reset on a admin user
    @param id_: The identifier of the admin user
    @type id_: int
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'POST':
        return AdminUserPasswordResetHandler().reset(id_)


@app.route("/admin/<int:id_>/password/update", methods=['POST'])
@authentication
def admin_password_update(id_: int) -> dict:
    """
    Route for password reset on a admin user
    @param id_: The identifier of the admin user
    @type id_: int
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'POST':
        user_id = request.get_json()["id"]
        password = request.get_json()["password"]
        return AdminUserPasswordResetHandler().change(id_, password)


@app.route("/admins", methods=['GET'])
@cache.cached(config.cache_timeout, unless=cache_bypass, query_string=True)
@authentication
def admins() -> dict:
    """
    Getting all the adminUsers objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return AdminUserHandler().get_all(request.args)


@app.route("/admin/add", methods=['POST'])
@authentication
def addAdmin() -> dict:
    """
    Adding a new user in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    cache.clear()
    return AdminUserHandler().post(request.get_json())


@app.route("/profile/add", methods=['POST'])
@authentication
def addProfile() -> dict:
    """
    Adding a new user in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    cache.clear()
    return ProfileHandler().post(request.get_json())


@app.route("/profile/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
@cache.memoize(config.cache_timeout, unless=cache_bypass)
@authentication
def profile(id_: int) -> dict:
    """
    Route for get, post, put of profile elements.
    @param id_: The identifier of the user
    @type id_: int
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'GET':
        return ProfileHandler().get(id_)

    elif request.method == 'PUT':
        cache.clear()
        return ProfileHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        cache.clear()
        return ProfileHandler().delete(id_)


@app.route("/profiles", methods=['GET'])
@cache.cached(config.cache_timeout, unless=cache_bypass, query_string=True)
@authentication
def profiles() -> dict:
    """
    Getting all the Profile objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return ProfileHandler().get_all(request.args)


@app.route("/subject/add", methods=['POST'])
@authentication
def addSubject() -> dict:
    """
    Adding a new user in the database
    @return: Custom Response message that we get from the handler class.
    @rtype: dict
    """
    cache.clear()
    return SubjectHandler().post(request.get_json())


@app.route("/subject/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
@cache.memoize(config.cache_timeout, unless=cache_bypass)
@authentication
def subject(id_: int) -> dict:
    """
    Route for get, post, put of profile elements.
    @param id_: The identifier of the user
    @type id_: int
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'GET':
        return SubjectHandler().get(id_)

    elif request.method == 'PUT':
        cache.clear()
        return SubjectHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        cache.clear()
        return SubjectHandler().delete(id_)


@app.route("/subjects", methods=['GET'])
@cache.cached(config.cache_timeout, unless=cache_bypass, query_string=True)
@authentication
def subjects() -> dict:
    """
    Getting all the Subject objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return SubjectHandler().get_all(request.args)


# Task
@app.route("/task/add", methods=['POST'])
@authentication
def addTask() -> dict:
    """
    Adding a new Task in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    cache.clear()
    return TaskHandler().post(request.get_json())


@app.route("/task/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
@cache.memoize(config.cache_timeout, unless=cache_bypass)
@authentication
def task(id_: int) -> dict:
    """
    Route for get, post, put of Task elements.
    @param id_: The identifier of the user
    @type id_: int
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'GET':
        return TaskHandler().get(id_)

    elif request.method == 'PUT':
        cache.clear()
        return TaskHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        cache.clear()
        return TaskHandler().delete(id_)


@app.route("/tasks", methods=['GET'])
@cache.cached(config.cache_timeout, unless=cache_bypass, query_string=True)
@authentication
def tasks() -> dict:
    """
    Getting all the Task objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return TaskHandler().get_all(request.args)


@app.route("/exercise/add", methods=['POST'])
@authentication
def addExercise() -> dict:
    """
    Adding a new Exercise in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    cache.clear()
    return ExerciseHandler().post(request.get_json())


@app.route("/exercise/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
@cache.memoize(config.cache_timeout, unless=cache_bypass)
@authentication
def exercise(id_: int) -> dict:
    """
    Route for get, post, put of Exercise elements.
    @param id_: The identifier of the user
    @type id_: int
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'GET':
        return ExerciseHandler().get(id_)

    elif request.method == 'PUT':
        cache.clear()
        return ExerciseHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        cache.clear()
        return ExerciseHandler().delete(id_)


@app.route("/exercises", methods=['GET'])
@cache.cached(config.cache_timeout, unless=cache_bypass, query_string=True)
@authentication
def exercises() -> dict:
    """
    Getting all the Exercise objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return ExerciseHandler().get_all(request.args)


@app.route("/file/upload", methods=["POST"])
@authentication
def uploadFile() -> dict:
    """
    Route to upload a file, that will be stored within the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'POST':
        return upload_file(request)


@app.route("/file/<int:id_>", methods=["GET", "DELETE"])
@cache.memoize(config.cache_timeout, unless=cache_bypass)
@authentication
def file(id_: int) -> dict:
    """
    Route for a deleting or getting a file.
    @param id_: The id of the file in the database
    @type id_: int
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'GET':
        data = FileHandler().get(id_)
        return send_file(io.BytesIO(data["file"]),
                         mimetype=mimetypes.guess_type(data["filename"])[0],
                         as_attachment=True,
                         download_name=(data["filename"]))

    elif request.method == 'DELETE':
        cache.clear()
        return FileHandler().delete(id_)


@app.route("/submission/add", methods=["POST"])
@authentication
def addSubmission() -> dict:
    """
    Add a submission to the DB
    @return: Response in form of dictionary
    @rtype: dict
    """
    cache.clear()
    if request.method == 'POST':
        output, response_code = SubmissionHandler().post(request.get_json())
        try:
            new_id = output["response"]["id"]
            SubmissionHandler().signal_execution_service(new_id)

        finally:
            return output


@app.route("/submission/<int:id_>", methods=["GET"])
@cache.memoize(config.cache_timeout, unless=cache_bypass)
@authentication
def submission(id_) -> dict:
    """
    Handler for get of a Submission
    @param id_: The id_ of the submission to get
    @type  id_: int
    @return: The JSON representation of the submission
    @rtype: dict
    """
    if request.method == 'GET':
        return SubmissionHandler().get(id_)


@app.route("/submissions", methods=['GET'])
@cache.cached(config.cache_timeout, unless=cache_bypass, query_string=True)
@authentication
def submissions() -> dict:
    """
    Getting all the Submission objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return SubmissionHandler().get_all(request.args)


@app.route("/testcase/add", methods=["POST"])
@authentication
def addTestCase() -> dict:
    """
    Add a TestCase to the DB
    @return: Response in form of dictionary
    @rtype: dict
    """
    cache.clear()
    if request.method == 'POST':
        return TestCaseHandler().post(request.get_json())


@app.route("/testcase/<int:id_>", methods=["GET", "DELETE"])
@cache.memoize(config.cache_timeout, unless=cache_bypass)
@authentication
def testcase(id_) -> dict:
    """
    Handler for get of a TestCase
    @param id_: The id_ of the TestCase to get
    @type  id_: int
    @return: The JSON representation of the TestCase
    @rtype: dict
    """
    if request.method == 'GET':
        return TestCaseHandler().get(id_)

    elif request.method == "DELETE":
        cache.clear()
        return TestCaseHandler().delete(id_)


@app.route("/testcases", methods=['GET'])
@authentication
def testcases() -> dict:
    """
    Getting all the TestCases objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return TestCaseHandler().get_all(request.args)


@app.route("/adminTypes", methods=['GET'])
@cache.cached(config.cache_timeout, unless=cache_bypass, query_string=True)
@authentication
def admin_types() -> dict:
    """
    Getting all the admin_types out of the database
    @@return: Custom Representation of all the objects
    @rtype: dict
    """
    return AdminTypeHandler().get_all(request.args)


@app.route("/task/<int:task_id_>/attachment/add", methods=["POST"])
@authentication
def task_attachment_add(task_id_: int) -> dict:
    """
    Adding an Attachment to a task
    Using seperate method to first add the task and then create the link entry in the table between task and file
    @param task_id_: The id_ of the task
    @type task_id_: int
    @return: Response in form of dictionary
    @rtype: dict
    """
    cache.clear()
    if request.method == 'POST':
        file_response = upload_file(request)[0]
        file_id = file_response["response"]["id"]
        attachment_data = request.form.to_dict()
        attachment_data = json.loads(attachment_data["data"].replace("\'", "\""))
        attachment_data['file_id'] = int(file_id)

        return AttachmentHandler().post(attachment_data)


@app.route("/task/<int:task_id_>/attachment/<int:attachment_id_>", methods=["GET", "DELETE"])
@cache.memoize(config.cache_timeout, unless=cache_bypass)
@authentication
def task_attachment(task_id_: int, attachment_id_: int) -> dict:
    """
    Adding an Attachment to a task
    @param task_id_: The id of the task
    @type task_id_: int
    @param attachment_id_: The id of the attachment
    @type attachment_id_: int
    @return: Response in form of dictionary
    @rtype: dict
    """
    if request.method == 'GET':
        return AttachmentHandler().get(attachment_id_)
    elif request.method == 'DELETE':
        cache.clear()
        return AttachmentHandler().delete(attachment_id_)
        # deletion of file not needed because it is made automatically due to datamodel


@app.route("/task/<int:task_id_>/instruction/add", methods=["POST"])
@authentication
def task_instruction_add(task_id_: int) -> dict:
    """
    Adding an Attachment to a task
    @param task_id_: The id_ of the task
    @type task_id_: int
    @return: Response in form of dictionary
    @rtype: dict
    """
    cache.clear()
    if request.method == 'POST':
        instruction_data = preprocess_task_file(request)
        return InstructionHandler().post(instruction_data)


@app.route("/task/<int:task_id_>/instruction/<int:instruction_id_>", methods=["GET", "DELETE"])
@cache.memoize(config.cache_timeout, unless=cache_bypass)
@authentication
def task_instruction(task_id_: int, instruction_id_: int) -> dict:
    """
    Adding an Attachment to a task
    @param task_id_: The id of the task
    @type task_id_: int
    @param instruction_id_: The id of the instruction
    @type instruction_id_: int
    @return: Response in form of dictionary
    @rtype: dict
    """
    if request.method == 'GET':
        return InstructionHandler().get(instruction_id_)
    elif request.method == 'DELETE':
        cache.clear()
        return InstructionHandler().delete(instruction_id_)
        # deletion of file not needed because it is made automatically due to datamodel


@app.route("/scores/<view>", methods=['GET'])
@authentication
def scores(view: str) -> dict:
    """
    Path for the rendering of scores with provided arguments in the url.
    @param view: What type of view must be rendered
    @type view: str
    @return: Reponse in form of a dictionary with the rendered scores
    @rtype: dict
    """
    return ScoreHandler().get_scores(view, request.args)


@app.route("/memberships", methods=['GET'])
@authentication
def memberships() -> dict:
    """
    Path for the rendering of all the memberships
    @return: A JSON with all the rendered Dictionaries
    @rtype: dict
    """
    if request.method == 'GET':
        return MembershipHandler().get_all(request.args)


@app.route("/membership/add", methods=['POST'])
@authentication
def addMembership() -> dict:
    """
    Path for creating a new membership in the database
    @return: A JSON with all the rendered Dictionaries
    @rtype: dict
    """
    if request.method == 'POST':
        return MembershipHandler().post(request.get_json())


@app.route("/membership/<int:id_>", methods=['GET','PUT', 'DELETE'])
@authentication
def membership(id_: int) -> dict:
    """
    Path for getting, updating and deleting a membership for a user to a subject.
    @param id_: The id of the membership in the database
    @type id_: int
    @return: A JSON with all the rendered Dictionaries
    @rtype: dict
    """
    if request.method == 'GET':
        return MembershipHandler().get(id_)

    elif request.method == 'PUT':
        return MembershipHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return MembershipHandler().delete(id_)


def api_backend() -> None:
    http_server = WSGIServer(("0.0.0.0", int(config.ApiPort)), app)
    print("WSGI SERVER started!")
    print(f"TIME: {datetime.datetime.now()}")
    print(f"PORT: {config.ApiPort}")
    http_server.serve_forever()


# starting the web application
if __name__ == "__main__":
    api_backend()
