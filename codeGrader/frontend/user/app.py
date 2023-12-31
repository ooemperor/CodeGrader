"""
Route defintion of the User Frontend of the CodeGrader
@author: mkaiser
@version: 1.0
"""

import flask_login
from flask import Flask, request, render_template, url_for, redirect, flash, session, Response
from flask_login import LoginManager, login_user, login_required, logout_user
from codeGrader.frontend.config import config
from codeGrader.frontend.user import templates
from codeGrader.frontend.user.handlers import UserSessionHandler, SessionUser, UserLoginHandler, HomeHandler, \
    ExerciseListHandler, ExerciseHandler, TaskHandler, TaskListHandler, TaskAttachmentHandler, TaskInstructionHandler, \
    AddSubmissionHandler
from gevent.pywsgi import WSGIServer
from typing import Union

app = Flask(config.userAppName, template_folder=templates.__path__[0])

# configuration of the login_manager and attaching it to the app
app.secret_key = config.userSecretKey
login_manager = LoginManager()
login_manager.init_app(app)


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
    @return: The rendered Task site
    @rtype: str
    """
    if request.method == 'GET':
        return TaskHandler(request).get(id_)


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


@app.route("/task/<int:task_id_>/submission/add", methods = ['POST'])
@login_required
def addSubmission(task_id_: int) -> Union[Response, str]:
    if request.method == 'POST':
        return AddSubmissionHandler(request).post(task_id_)


def user_frontend():
    http_server = WSGIServer(("0.0.0.0", int(config.userPort)), app)
    http_server.serve_forever()


if __name__ == "__main__":
    user_frontend()
