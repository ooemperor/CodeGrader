"""
Route definition and main File that runs the application.
@author: mkaiser
@version: 1.0
"""
import io
import mimetypes

from flask import Flask, request, send_file
from codeGrader.backend.config import config
from codeGrader.backend.api.handlers import UserHandler, ProfileHandler, AdminUserHandler, SubjectHandler, \
    ExerciseHandler, TaskHandler, FileHandler
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
def home():
    """
    Returns the home Data.
    :return: The home Data for testing purposes
    """
    if request.method == "POST":
        print(request.get_json())
        return "Success!"

    else:
        response = {"text": "Hello World"}
        return response
    # TODO: remove home directory after paths are implement.


# TODO: Add all the routes needed for the backend API


@app.route("/user/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
def user(id_: int):
    """
    Route for get, post, put of user elements.
    @param id_: The identifier of the user
    @type id_: int
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    log.info(f"{request.remote_addr} {request.method} {request.path}")
    if request.method == 'GET':
        return UserHandler().get(id_)

    elif request.method == 'PUT':
        return UserHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return UserHandler().delete(id_)


@app.route("/addUser", methods=['POST'])
def addUser():
    """
    Adding a new user in the database
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    log.info(f"{request.remote_addr} {request.method} {request.path}")
    return UserHandler().post(request.get_json())


@app.route("/adminUser/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
def adminUser(id_: int):
    """
    Route for get, post, put of user elements.
    @param id_: The identifier of the user
    @type id_: int
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    log.info(f"{request.remote_addr} {request.method} {request.path}")
    if request.method == 'GET':
        return AdminUserHandler().get(id_)

    elif request.method == 'PUT':
        return AdminUserHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return AdminUserHandler().delete(id_)


@app.route("/addAdminUser", methods=['POST'])
def addAdminUser():
    """
    Adding a new user in the database
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    log.info(f"{request.remote_addr} {request.method} {request.path}")
    return AdminUserHandler().post(request.get_json())


@app.route("/addProfile", methods=['POST'])
def addProfile():
    """
    Adding a new user in the database
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    log.info(f"{request.remote_addr} {request.method} {request.path}")
    return ProfileHandler().post(request.get_json())


@app.route("/profile/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
def profile(id_: int):
    """
    Route for get, post, put of profile elements.
    @param id_: The identifier of the user
    @type id_: int
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    log.info(f"{request.remote_addr} {request.method} {request.path}")
    if request.method == 'GET':
        return ProfileHandler().get(id_)

    elif request.method == 'PUT':
        return ProfileHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return ProfileHandler().delete(id_)


@app.route("/addSubject", methods=['POST'])
def addSubject():
    """
    Adding a new user in the database
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    log.info(f"{request.remote_addr} {request.method} {request.path}")
    return SubjectHandler().post(request.get_json())


@app.route("/subject/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
def subject(id_: int):
    """
    Route for get, post, put of profile elements.
    @param id_: The identifier of the user
    @type id_: int
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    log.info(f"{request.remote_addr} {request.method} {request.path}")
    if request.method == 'GET':
        return SubjectHandler().get(id_)

    elif request.method == 'PUT':
        return SubjectHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return SubjectHandler().delete(id_)


# Task
@app.route("/addTask", methods=['POST'])
def addTask():
    """
    Adding a new Task in the database
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    log.info(f"{request.remote_addr} {request.method} {request.path}")
    return TaskHandler().post(request.get_json())


@app.route("/task/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
def task(id_: int):
    """
    Route for get, post, put of Task elements.
    @param id_: The identifier of the user
    @type id_: int
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    if request.method == 'GET':
        return TaskHandler().get(id_)

    elif request.method == 'PUT':
        return TaskHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return TaskHandler().delete(id_)


@app.route("/addExercise", methods=['POST'])
def addExercise():
    """
    Adding a new Exercise in the database
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    return ExerciseHandler().post(request.get_json())


@app.route("/exercise/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
def exercise(id_: int):
    """
    Route for get, post, put of Exercise elements.
    @param id_: The identifier of the user
    @type id_: int
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    log.info(f"{request.remote_addr} {request.method} {request.path}")
    if request.method == 'GET':
        return ExerciseHandler().get(id_)

    elif request.method == 'PUT':
        return ExerciseHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return ExerciseHandler().delete(id_)


@app.route("/uploadFile", methods=["POST"])
def uploadFile():
    if request.method == 'POST':
        if len(request.files.keys()) > 1:
            return "Error", 500
        else:
            file_ = request.files[list(request.files.keys())[0]]
            file_type = file_.filename.rsplit('.', 1)[1].lower()
            data = {"filename": file_.filename, "fileExtension": file_type, "file": file_.read()}
            return FileHandler().post(data)

    else:
        # TODO: return error for wrong method.
        return "Error", 500


@app.route("/file/<int:id_>", methods=["GET", "DELETE"])
def file(id_: int):
    """

    @param id_: The id of the file in the database
    @type id_: int
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    if request.method == 'GET':
        data = FileHandler().get(id_)
        return send_file(io.BytesIO(data["file"]),
                         mimetype=mimetypes.guess_type(data["filename"])[0],
                         as_attachment=True,
                         download_name=(data["filename"]))

    elif request.method == 'DELETE':
        return FileHandler().delete(id_)

    else:
        # TODO: return error for wrong method.
        return "Error", 500


# starting the web application
if __name__ == "__main__":
    app.run(port=config.ApiPort, debug=config.debug)
