"""
Route definition and main File that runs the application.
@author: mkaiser
@version: 1.0
"""

from flask import Flask, request
from config import config
from handlers.User import UserHandler


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
        print(request.get_json())
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


# starting the web application
app.run(port=config.port, debug=config.debug)
