"""
Route definition and main File that runs the application.
@author: mkaiser
@version: 1.0
"""
import io
import mimetypes
from functools import wraps

from flask import Flask, request, send_file
from codeGrader.backend.config import config
from codeGrader.backend.api.handlers import UserHandler, ProfileHandler, AdminUserHandler, SubjectHandler, \
    ExerciseHandler, TaskHandler, FileHandler, SubmissionHandler, TestCaseHandler, AdminUserLoginHandler, authentication
from codeGrader.backend.api.logger import Logger
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


@app.route("/login", methods=['POST'])
def login():
    """
    Login for a provided user
    """
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    return AdminUserLoginHandler().login(username, password)


@app.route("/user/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
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
def users():
    """
    Getting all the users objects out of the database
    @return: Custom Representation of all the user objects
    @rtype: dict
    """
    return UserHandler().get_all()


@app.route("/addUser", methods=['POST'])
def addUser():
    """
    Adding a new user in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    return UserHandler().post(request.get_json())


@app.route("/adminUser/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
def adminUser(id_: int):
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


@app.route("/adminUsers", methods=['GET'])
def adminUsers():
    """
    Getting all the adminUsers objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return AdminUserHandler().get_all()


@app.route("/addAdminUser", methods=['POST'])
def addAdminUser():
    """
    Adding a new user in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    return AdminUserHandler().post(request.get_json())


@app.route("/addProfile", methods=['POST'])
def addProfile():
    """
    Adding a new user in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    return ProfileHandler().post(request.get_json())


@app.route("/profile/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
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
def profiles():
    """
    Getting all the Profile objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return ProfileHandler().get_all()


@app.route("/addSubject", methods=['POST'])
def addSubject():
    """
    Adding a new user in the database
    @return: Custom Response message that we get from the handler class.
    @rtype: dict
    """
    return SubjectHandler().post(request.get_json())


@app.route("/subject/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
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
def subjects():
    """
    Getting all the Subject objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return SubjectHandler().get_all()


# Task
@app.route("/addTask", methods=['POST'])
def addTask():
    """
    Adding a new Task in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    return TaskHandler().post(request.get_json())


@app.route("/task/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
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
def tasks():
    """
    Getting all the Task objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return TaskHandler().get_all()


@app.route("/addExercise", methods=['POST'])
def addExercise():
    """
    Adding a new Exercise in the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    return ExerciseHandler().post(request.get_json())


@app.route("/exercise/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
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
def exercises():
    """
    Getting all the Exercise objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return ExerciseHandler().get_all()


@app.route("/uploadFile", methods=["POST"])
def uploadFile():
    """
    Route to upload a file, that will be stored within the database
    @return: Custom Response messgae that we get from the handler class.
    @rtype: dict
    """
    if request.method == 'POST':
        if len(request.files.keys()) > 1:
            return "Error", 500
        else:
            file_ = request.files[list(request.files.keys())[0]]
            file_type = file_.filename.rsplit('.', 1)[1].lower()
            data = {"filename": file_.filename, "fileExtension": file_type, "file": file_.read()}
            return FileHandler().post(data)



@app.route("/file/<int:id_>", methods=["GET", "DELETE"])
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


@app.route("/addSubmission", methods=["POST"])
def addSubmission():
    """
    Add a submission to the DB
    @return: Response in form of dictionary
    @rtype: dict
    """
    if request.method == 'POST':
        return SubmissionHandler().post(request.get_json())


@app.route("/submission/<int:id_>", methods=["GET"])
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
def submissions():
    """
    Getting all the Submission objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return SubmissionHandler().get_all()


@app.route("/addTestCase", methods=["POST"])
def addTestCase():
    """
    Add a TestCase to the DB
    @return: Response in form of dictionary
    @rtype: dict
    """
    if request.method == 'POST':
        return TestCaseHandler().post(request.get_json())


@app.route("/testcase/<int:id_>", methods=["GET"])
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
def testcases():
    """
    Getting all the TestCases objects out of the database
    @return: Custom Representation of all the objects
    @rtype: dict
    """
    return TestCaseHandler().get_all()


# starting the web application
if __name__ == "__main__":
    app.run(port=config.ApiPort, debug=config.debug)
