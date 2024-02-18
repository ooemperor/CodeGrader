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
Route defintion of the User Frontend of the CodeGrader
@author: mkaiser
@version: 1.0
"""

import flask_login
from flask import Flask, request, render_template, url_for, redirect, flash, session, Response
from flask_login import LoginManager, login_user, login_required, logout_user
from codeGrader.frontend.config import config
from codeGrader.frontend.user.handlers import UserSessionHandler, SessionUser, UserLoginHandler, HomeHandler, \
    ExerciseListHandler, ExerciseHandler, TaskHandler, TaskListHandler, TaskAttachmentHandler, TaskInstructionHandler, \
    AddSubmissionHandler, SettingsHandler, PasswordResetHandler, SubjectHandler, SubjectListHandler, SubmissionHandler, \
    ErrorHandler
from gevent.pywsgi import WSGIServer
from typing import Union
import datetime

app = Flask(config.userAppName, template_folder="./templates")

# configuration of the login_manager and attaching it to the app
app.secret_key = config.userSecretKey
login_manager = LoginManager()
login_manager.init_app(app)


@app.context_processor
def global_vars():
    """
    Returns a dictionary with global variables that we can use in the templates rendering
    uses builtin decorator from flask
    @return: Global Variables dictionary for rendering
    @rtype: dict
    """
    return dict(appname=config.userAppName)


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


@login_manager.user_loader
def user_login(user_id: int):
    """
    User Load of the Login Manager
    Returns the Frontend Representation of a User
    @param user_id: The id of the user
    @type user_id: int
    @return: The frontend user object
    @rtype: SessionUser
    """
    user = SessionUser(user_id)
    return user


@login_manager.unauthorized_handler
def unauthorized():
    """
    Returns to login page if you are not properly logged in
    @return: Redirection to the login site.
    """
    return redirect(url_for("login"))


@app.errorhandler(Exception)
def error(err: Exception):
    """
    Error Handler for a when a error occurs.
    @param err: The Exception that has been raised
    @type err: Exception
    @return: Rendered Error Page with Information for the user
    """
    return ErrorHandler(request).get(err, err.code)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Renders the login page on GET
    Tries to log the user in on POST
    @return: Rendered template or a redirection
    """
    if request.method == 'GET':
        return render_template("login.html")

    elif request.method == 'POST':
        # try to log the user in
        user_id = UserLoginHandler(request).post()
        if user_id:
            user = user_login(user_id)
            login_user(user)
        else:
            flash("The provided Credentials are not valid")
        return redirect(url_for("home"))


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    """
    Logout a user so he needs to reauthenticate
    @return: Redirect to the login page
    """
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    """
    The Home site of the user frontend
    @return: Rendered Home Template
    """
    return HomeHandler(request).get()


@app.route("/subjects", methods=['GET'])
@login_required
def subjects() -> str:
    """
    The SubjectListHandler to render or redirect the templates.
    @return: The rendered Subjects site
    @rtype: str
    """
    return SubjectListHandler(request).get()


@app.route("/subject/<int:id_>", methods=['GET'])
@login_required
def subject(id_: int) -> str:
    """
    The SubjectHandler to render or redirect the templates
    @param id_: The identifier of the subject
    @type id_: int
    @return: The rendered Subject site
    @rtype: str
    """
    if request.method == 'GET':
        return SubjectHandler(request).get(id_)


@app.route("/exercises", methods=['GET'])
@login_required
def exercises() -> str:
    """
    The ExercisesListHandler to render or redirect the templates.
    @return: The rendered Exercises site
    @rtype: str
    """
    return ExerciseListHandler(request).get()


@app.route("/exercise/<int:id_>", methods=['GET'])
@login_required
def exercise(id_: int) -> str:
    """
    The ExerciseHandler to render or redirect the templates
    @param id_: The identifier of the exercise
    @type id_: int
    @return: The rendered Exercise site
    @rtype: str
    """
    if request.method == 'GET':
        return ExerciseHandler(request).get(id_)


@app.route("/tasks", methods=['GET'])
@login_required
def tasks() -> str:
    """
    The TaskListHandler to render or redirect the templates.
    @return: The rendered Tasks site
    @rtype: str
    """
    return TaskListHandler(request).get()


@app.route("/task/<int:id_>", methods=['GET'])
@login_required
def task(id_: int) -> str:
    """
    The TaskHandler to render or redirect the templates
    @param id_: The identifier of the task
    @type id_: int
    @param submission_id: The id of a submission if a submission has been made (used for rendering after submission)
    @type submission_id: int
    @return: The rendered Task site
    @rtype: str
    """
    if request.method == 'GET':
        return TaskHandler(request).get(id_, request.args)


@app.route("/task/<int:task_id_>/attachment/<int:attachment_id_>", methods=['GET'])
@login_required
def TaskAttachment(task_id_: int, attachment_id_: int) -> Union[Response, str]:
    """
    Adding an Attachment File to a Task
    @param task_id_: The id of the task
    @type task_id_: int
    @param attachment_id_: The id of the Attachment
    @type attachment_id_: int
    @return: Redirect to another view
    @rtype: Response/str
    """
    if request.method == 'GET':
        return TaskAttachmentHandler(request).get(task_id_, attachment_id_)


@app.route("/task/<int:task_id_>/instruction/<int:instruction_id_>", methods=['GET'])
@login_required
def TaskInstruction(task_id_: int, instruction_id_: int) -> Union[Response, str]:
    """
    Getting the file for a Task Instruction
    @param task_id_: The id of the task
    @type task_id_: int
    @param instruction_id_: The id of the Attachment
    @type instruction_id_: int
    @return: Redirect to another view
    @rtype: Response/str
    """
    if request.method == 'GET':
        return TaskInstructionHandler(request).get(task_id_, instruction_id_)


@app.route("/task/<int:task_id_>/submission/add", methods=['POST'])
@login_required
def addSubmission(task_id_: int) -> Union[Response, str]:
    if request.method == 'POST':
        return AddSubmissionHandler(request).post(task_id_)


@app.route("/gamification/submission/<int:id_>", methods=['GET'])
@login_required
def submission_gamification(id_: int) -> Union[Response, str]:
    """
    Route for the function that returns HTML code to be inserted by javascript into the code
    @param id_: The identifier of the submission that has been made
    @type id_: int
    @return: HTML Code
    @rtype: str
    """
    if request.method == 'GET':
        return SubmissionHandler(request).get_gamification(id_)


@app.route("/settings", methods=['GET'])
@login_required
def settings():
    if request.method == 'GET':
        return SettingsHandler(request).get()


@app.route("/passwordreset", methods=['POST'])
@login_required
def password_reset() -> Response:
    """
    Route to reset a password of a user that is already logged in
    @return: Redirect back to the settings page with a distinct flash messaage
    """
    if request.method == 'POST':
        return PasswordResetHandler(request).post()


def user_frontend():
    http_server = WSGIServer(("0.0.0.0", int(config.userPort)), app)
    print("WSGI SERVER started!")
    print(f"TIME: {datetime.datetime.now()}")
    print(f"PORT: {config.userPort}")
    http_server.serve_forever()


if __name__ == "__main__":
    user_frontend()
