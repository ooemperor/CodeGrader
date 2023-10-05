"""
Route definition and main File that runs the application.
@author: mkaiser
@version: 1.0
"""

from flask import Flask, request, send_file
from config import config
from handlers import UserHandler, ProfileHandler, AdminUserHandler, SubjectHandler, ExerciseHandler, TaskHandler


# construction of Application and DB Connection
app = Flask(config.appName)


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
def user(id_):
    """
    Route for get, post, put of user elements.
    @param id_: The identifier of the user
    @return: # TODO: define return type of api
    @rtype: undefined
    """
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
    return UserHandler().post(request.get_json())


@app.route("/adminUser/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
def adminUser(id_):
    """
    Route for get, post, put of user elements.
    @param id_: The identifier of the user
    @return: # TODO: define return type of api
    @rtype: undefined
    """
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
    return AdminUserHandler().post(request.get_json())


@app.route("/addProfile", methods=['POST'])
def addProfile():
    """
    Adding a new user in the database
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    return ProfileHandler().post(request.get_json())


@app.route("/profile/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
def profile(id_):
    """
    Route for get, post, put of profile elements.
    @param id_: The identifier of the user
    @return: # TODO: define return type of api
    @rtype: undefined
    """
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
    return SubjectHandler().post(request.get_json())


@app.route("/subject/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
def subject(id_):
    """
    Route for get, post, put of profile elements.
    @param id_: The identifier of the user
    @return: # TODO: define return type of api
    @rtype: undefined
    """
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
    return TaskHandler().post(request.get_json())


@app.route("/task/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
def task(id_):
    """
    Route for get, post, put of Task elements.
    @param id_: The identifier of the user
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
    return TaskHandler().post(request.get_json())


@app.route("/exercise/<int:id_>", methods=['GET', 'PUT', 'DELETE'])
def exercise(id_):
    """
    Route for get, post, put of Exercise elements.
    @param id_: The identifier of the user
    @return: # TODO: define return type of api
    @rtype: undefined
    """
    if request.method == 'GET':
        return ExerciseHandler().get(id_)

    elif request.method == 'PUT':
        return ExerciseHandler().put(id_, request.get_json())

    elif request.method == 'DELETE':
        return ExerciseHandler().delete(id_)

# starting the web application
app.run(port=config.port, debug=config.debug)
