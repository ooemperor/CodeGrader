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
from codeGrader.backend.config import config
from codeGrader.backend.api.handlers import UserHandler, ProfileHandler, AdminUserHandler, SubjectHandler, \
    ExerciseHandler, TaskHandler, FileHandler, SubmissionHandler, TestCaseHandler, AdminUserLoginHandler, \
    authentication, AdminTypeHandler, UserLoginHandler, InstructionHandler, AttachmentHandler
from codeGrader.backend.api.logger import Logger
from codeGrader.backend.api.util import upload_file, preprocess_task_file
import logging

# construction of Application and DB Connection
app = Flask(config.appName)

# disabling the integrated logger if set so in the config. 
if not config.useIntegratedLogin:
    app.logger.disabled = True
    log = logging.getLogger('werkzeug')
    log.disabled = True

# adding the custom logger
log = Logger()


@app.route("/", methods=['POST', 'GET'])
@authentication
def home():
    """
    Returns the answer to all questions
    @return: The answer to all the questions
    """
    response = {"response": "42"}
    return response


@app.route("/admin/login", methods=['POST'])
@authentication
def admin_login():
    """
    Login for a provided Admin User
    """
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    return AdminUserLoginHandler().login(username, password)


@app.route("/user/login", methods=['POST'])
@authentication
def user_login():
    """
    Login for a provided user
    """
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    return UserLoginHandler().login(username, password)


@app.route("/user/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
@authentication
def user(id_: int):
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
        return UserHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return UserHandler().delete(id_)


@app.route("/users", methods=['GET'])
@authentication
def users():
    """
    Getting all the users objects out of the database
    @return: Custom Representation of all the user objects
    @rtype: dict
    """
    return UserHandler().get_all(request.args)


@app.route("/user/add", methods=['POST'])
@authentication
def addUser():
    """
    Adding a new user in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    return UserHandler().post(request.get_json())


@app.route("/admin/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
@authentication
def admin(id_: int):
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
        return AdminUserHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return AdminUserHandler().delete(id_)


@app.route("/admins", methods=['GET'])
@authentication
def admins():
    """
    Getting all the adminUsers objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return AdminUserHandler().get_all(request.args)


@app.route("/admin/add", methods=['POST'])
@authentication
def addAdmin():
    """
    Adding a new user in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    return AdminUserHandler().post(request.get_json())


@app.route("/profile/add", methods=['POST'])
@authentication
def addProfile():
    """
    Adding a new user in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    return ProfileHandler().post(request.get_json())


@app.route("/profile/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
@authentication
def profile(id_: int):
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
        return ProfileHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return ProfileHandler().delete(id_)


@app.route("/profiles", methods=['GET'])
@authentication
def profiles():
    """
    Getting all the Profile objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return ProfileHandler().get_all(request.args)


@app.route("/subject/add", methods=['POST'])
@authentication
def addSubject():
    """
    Adding a new user in the database
    @return: Custom Response message that we get from the handler class.
    @rtype: dict
    """
    return SubjectHandler().post(request.get_json())


@app.route("/subject/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
@authentication
def subject(id_: int):
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
        return SubjectHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return SubjectHandler().delete(id_)


@app.route("/subjects", methods=['GET'])
@authentication
def subjects():
    """
    Getting all the Subject objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return SubjectHandler().get_all(request.args)


# Task
@app.route("/task/add", methods=['POST'])
@authentication
def addTask():
    """
    Adding a new Task in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    return TaskHandler().post(request.get_json())


@app.route("/task/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
@authentication
def task(id_: int):
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
        return TaskHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return TaskHandler().delete(id_)


@app.route("/tasks", methods=['GET'])
@authentication
def tasks():
    """
    Getting all the Task objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return TaskHandler().get_all(request.args)


@app.route("/exercise/add", methods=['POST'])
@authentication
def addExercise():
    """
    Adding a new Exercise in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    return ExerciseHandler().post(request.get_json())


@app.route("/exercise/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
@authentication
def exercise(id_: int):
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
        return ExerciseHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return ExerciseHandler().delete(id_)


@app.route("/exercises", methods=['GET'])
@authentication
def exercises():
    """
    Getting all the Exercise objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return ExerciseHandler().get_all(request.args)


@app.route("/file/upload", methods=["POST"])
@authentication
def uploadFile():
    """
    Route to upload a file, that will be stored within the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'POST':
        return upload_file(request)


@app.route("/file/<int:id_>", methods=["GET", "DELETE"])
@authentication
def file(id_: int):
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
        return FileHandler().delete(id_)


@app.route("/submission/add", methods=["POST"])
@authentication
def addSubmission():
    """
    Add a submission to the DB
    @return: Response in form of dictionary
    @rtype: dict
    """
    if request.method == 'POST':
        output, response_code = SubmissionHandler().post(request.get_json())
        try:
            new_id = output["response"]["id"]
            SubmissionHandler().signal_execution_service(new_id)

        finally:
            return output


@app.route("/submission/<int:id_>", methods=["GET"])
@authentication
def submission(id_):
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
@authentication
def submissions():
    """
    Getting all the Submission objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return SubmissionHandler().get_all(request.args)


@app.route("/testcase/add", methods=["POST"])
@authentication
def addTestCase():
    """
    Add a TestCase to the DB
    @return: Response in form of dictionary
    @rtype: dict
    """
    if request.method == 'POST':
        return TestCaseHandler().post(request.get_json())


@app.route("/testcase/<int:id_>", methods=["GET"])
@authentication
def testcase(id_):
    """
    Handler for get of a TestCase
    @param id_: The id_ of the TestCase to get
    @type  id_: int
    @return: The JSON representation of the TestCase
    @rtype: dict
    """
    if request.method == 'GET':
        return TestCaseHandler().get(id_)


@app.route("/testcases", methods=['GET'])
@authentication
def testcases():
    """
    Getting all the TestCases objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return TestCaseHandler().get_all(request.args)


@app.route("/adminTypes", methods=['GET'])
@authentication
def admin_types():
    """
    Getting all the admin_types out of the database
    @@return: Custom Representation of all the objects
    @rtype: dict
    """
    return AdminTypeHandler().get_all(request.args)


@app.route("/task/<int:task_id_>/attachment/add", methods=["POST"])
@authentication
def task_attachment_add(task_id_: int):
    """
    Adding an Attachment to a task
    Using seperate method to first add the task and then create the link entry in the table between task and file
    @param task_id_: The id_ of the task
    @type task_id_: int
    @return: Response in form of dictionary
    @rtype: dict
    """
    if request.method == 'POST':
        file_response = upload_file(request)[0]
        file_id = file_response["response"]["id"]
        attachment_data = request.form.to_dict()
        attachment_data = json.loads(attachment_data["data"].replace("\'", "\""))
        attachment_data['file_id'] = int(file_id)

        return AttachmentHandler().post(attachment_data)


@app.route("/task/<int:task_id_>/attachment/<int:attachment_id_>", methods=["GET", "DELETE"])
@authentication
def task_attachment(task_id_: int, attachment_id_: int):
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
        return AttachmentHandler().delete(attachment_id_)
        # deletion of file not needed because it is made automatically due to datamodel


@app.route("/task/<int:task_id_>/instruction/add", methods=["POST"])
@authentication
def task_instruction_add(task_id_: int):
    """
    Adding an Attachment to a task
    @param task_id_: The id_ of the task
    @type task_id_: int
    @return: Response in form of dictionary
    @rtype: dict
    """
    if request.method == 'POST':
        instruction_data = preprocess_task_file(request)
        return InstructionHandler().post(instruction_data)


@app.route("/task/<int:task_id_>/instruction/<int:instruction_id_>", methods=["GET", "DELETE"])
@authentication
def task_instruction(task_id_: int, instruction_id_: int):
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
        return InstructionHandler().delete(instruction_id_)
        # deletion of file not needed because it is made automatically due to datamodel


def api_backend():
    http_server = WSGIServer(("0.0.0.0", int(config.ApiPort)), app)
    http_server.serve_forever()


# starting the web application
if __name__ == "__main__":
    api_backend()
