"""
Route definition and main File for the Admin Frontend of the CodeGrader
@author: mkaiser
@version: 1.0
"""
import flask_login
from flask import Flask, request, render_template, url_for, redirect, flash, session, Response
from flask_login import LoginManager, login_user, login_required, logout_user
from typing import Union
from codeGrader.frontend.config import config
from codeGrader.frontend.admin import templates
from codeGrader.frontend.admin.handlers import AdminUserLoginHandler, AdminSessionHandler, SessionAdmin, \
    UserListHandler, UserHandler, HomeHandler, AdminListHandler, AdminHandler, ProfileListHandler, \
    ProfileHandler, SubjectListHandler, SubjectHandler, TaskHandler, TaskListHandler, ExerciseHandler, \
    ExerciseListHandler, AddAdminHandler, AddProfileHandler, AddUserHandler, AddTaskHandler, AddExerciseHandler, \
    AddSubjectHandler, DeleteUserHandler, DeleteSubjectHandler, DeleteAdminHandler, DeleteTaskHandler, \
    DeleteExerciseHandler, DeleteProfileHandler, AddTaskAttachmentHandler, DeleteTaskAttachmentHandler, \
    AddTaskInstructionHandler, DeleteTaskInstructionHandler, TaskInstructionHandler, TaskAttachmentHandler
from gevent.pywsgi import WSGIServer

app = Flask(config.adminAppName, template_folder=templates.__path__[0])

# configuration of the login_manager and attaching it to the app
app.secret_key = config.adminSecretKey
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def adminUser_login(admin_id):
    """
    User load of the login_manager
    Returns the frontend represenation of the admin user
    @param admin_id: the id of the user
    @type admin_id: int
    @return: The frontend User Object
    @rtype: SessionAdmin
    """
    user = SessionAdmin(admin_id)
    return user


@app.route("/login", methods=['GET', 'POST'])
def login() -> Union[Response, str]:
    """
    Renders the login page on GET
    Tries to log the user in on POST
    @return: Rendered template or a redirection
    """
    if request.method == 'GET':
        return render_template("login.html")

    elif request.method == 'POST':
        user_id = AdminUserLoginHandler(request).post()
        if user_id:
            user = adminUser_login(user_id)
            login_user(user)
        else:
            flash("The provided Credentials are not valid")
        return redirect(url_for("home"))


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout() -> Response:
    """
    Logout a user so he needs to reauthenticate
    @return: Redirect to the login page
    @rtype: Response
    """
    logout_user()
    return redirect(url_for("login"))


@login_manager.unauthorized_handler
def unauthorized() -> Response:
    """
    Returns to login page if you are not properly logged in
    @return: Redirection to the login site.
    """
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home() -> str:
    """
    The Home site of the admin frontend
    @return: Rendered Home Template
    """
    return HomeHandler(request).get()


@app.route("/user/<int:id_>", methods=['GET', 'POST'])
@login_required
def user(id_) -> Union[Response, str]:
    """
    TODO: correct this representation
    @param id_: The identifier of the user
    @type id_: int
    @return: The rendered User
    """
    if request.method == 'GET':
        return UserHandler(request).get(id_)
    elif request.method == 'POST':
        return UserHandler(request).post(id_)


@app.route("/users")
@login_required
def users() -> str:
    """
    Site to display all users
    @return: Rendered Users Site
    """
    return UserListHandler(request).get()


@app.route("/user/add", methods=['GET', 'POST'])
@login_required
def addUser() -> Union[Response, str]:
    """
    Site to add an User
    @return: Rendered Users site or redirect
    """
    if request.method == 'GET':
        return AddUserHandler(request).get()
    elif request.method == 'POST':
        return AddUserHandler(request).post()


@app.route("/user/delete/<int:id_>", methods=['GET', 'POST'])
@login_required
def deleteUser(id_: int) -> Union[Response, str]:
    """
    Deleting a user from the database
    @param id_: The identifier of the user
    @type id_: int
    @return: Redirect to another view.
    """
    if request.method == 'GET':
        return DeleteUserHandler(request).get(id_)
    elif request.method == 'POST':
        return DeleteUserHandler(request).post(id_)


@app.route("/admin/<int:id_>", methods=['GET', 'POST'])
@login_required
def admin(id_) -> Union[Response, str]:
    """
    @param id_: The identifier of the adminuser
    @type id_: int
    @return: The rendered adminUser
    """
    if request.method == 'GET':
        return AdminHandler(request).get(id_)
    elif request.method == 'POST':
        return AdminHandler(request).post(id_)


@app.route("/admins")
@login_required
def admins() -> str:
    """
    Site to display all Admins
    @return: Rendered AdminUsers Site
    """
    return AdminListHandler(request).get()


@app.route("/admin/add", methods=['GET', 'POST'])
@login_required
def addAdmin() -> Union[Response, str]:
    """
    Site to add an Admin User
    @return: Rendered Admin Users site or redirect
    """
    if request.method == 'GET':
        return AddAdminHandler(request).get()
    elif request.method == 'POST':
        return AddAdminHandler(request).post()


@app.route("/admin/delete/<int:id_>", methods=['GET', 'POST'])
@login_required
def deleteAdmin(id_: int) -> Union[Response, str]:
    """
    Deleting a Admin from the database
    @param id_: The identifier of the Admin
    @type id_: int
    @return: Redirect to another view.
    """
    if request.method == 'GET':
        return DeleteAdminHandler(request).get(id_)
    elif request.method == 'POST':
        return DeleteAdminHandler(request).post(id_)


@app.route("/profile/<int:id_>", methods=['GET', 'POST'])
@login_required
def profile(id_) -> Union[Response, str]:
    """
    Site to diplay a single
    @param id_: The id of the profile
    @type id_: int
    @return: The rendered Profile site
    """
    if request.method == 'GET':
        return ProfileHandler(request).get(id_)
    elif request.method == 'POST':
        return ProfileHandler(request).post(id_)


@app.route("/profiles")
@login_required
def profiles() -> str:
    """
    Site for a list of all the profiles
    @return: The rendered Profiles site
    """
    return ProfileListHandler(request).get()


@app.route("/profile/add", methods=['GET', 'POST'])
@login_required
def addProfile() -> Union[Response, str]:
    """
    Site to add a Profile
    @return: Rendered Profile site or redirect
    """
    if request.method == 'GET':
        return AddProfileHandler(request).get()
    elif request.method == 'POST':
        return AddProfileHandler(request).post()


@app.route("/profile/delete/<int:id_>", methods=['GET', 'POST'])
@login_required
def deleteProfile(id_: int) -> Union[Response, str]:
    """
    Deleting a profile from the database
    @param id_: The identifier of the profile
    @type id_: int
    @return: Redirect to another view.
    """
    if request.method == 'GET':
        return DeleteProfileHandler(request).get(id_)
    elif request.method == 'POST':
        return DeleteProfileHandler(request).post(id_)


@app.route("/subject/<int:id_>", methods=['GET', 'POST'])
@login_required
def subject(id_) -> Union[Response, str]:
    """
    Site to display a single subject
    @param id_: The id of the subject
    @type id_: int
    @return: The rendered Subject site
    """
    if request.method == 'GET':
        return SubjectHandler(request).get(id_)
    elif request.method == 'POST':
        return SubjectHandler(request).post(id_)


@app.route("/subjects")
@login_required
def subjects() -> str:
    """
    Site for a list of all the subjects
    @return: The rendered Subjects site
    """
    return SubjectListHandler(request).get()


@app.route("/subject/add", methods=['GET', 'POST'])
@login_required
def addSubject() -> Union[Response, str]:
    """
    Site to add a Subject
    @return: Rendered Subject site or redirect
    """
    if request.method == 'GET':
        return AddSubjectHandler(request).get()
    elif request.method == 'POST':
        return AddSubjectHandler(request).post()


@app.route("/subject/delete/<int:id_>", methods=['GET', 'POST'])
@login_required
def deleteSubject(id_: int) -> Union[Response, str]:
    """
    Deleting a subject from the database
    @param id_: The identifier of the subject
    @type id_: int
    @return: Redirect to another view.
    """
    if request.method == 'GET':
        return DeleteSubjectHandler(request).get(id_)
    elif request.method == 'POST':
        return DeleteSubjectHandler(request).post(id_)


@app.route("/exercise/<int:id_>", methods=['GET', 'POST'])
@login_required
def exercise(id_) -> Union[Response, str]:
    """
    Site to display a single exercise
    @param id_: The id of the exercise
    @type id_: int
    @return: The rendered exercise site
    """
    if request.method == 'GET':
        return ExerciseHandler(request).get(id_)
    elif request.method == 'POST':
        return ExerciseHandler(request).post(id_)


@app.route("/exercises")
@login_required
def exercises() -> str:
    """
    Site for a list of all the exercises
    @return: The rendered exercises site
    """
    return ExerciseListHandler(request).get()


@app.route("/exercise/add", methods=['GET', 'POST'])
@login_required
def addExercise() -> Union[Response, str]:
    """
    Site to add a Exercise
    @return: Rendered Exercise site or redirect
    """
    if request.method == 'GET':
        return AddExerciseHandler(request).get()
    elif request.method == 'POST':
        return AddExerciseHandler(request).post()


@app.route("/exercise/delete/<int:id_>", methods=['GET', 'POST'])
@login_required
def deleteExercise(id_: int) -> Union[Response, str]:
    """
    Deleting a exercise from the database
    @param id_: The identifier of the exercise
    @type id_: int
    @return: Redirect to another view.
    """
    if request.method == 'GET':
        return DeleteExerciseHandler(request).get(id_)
    elif request.method == 'POST':
        return DeleteExerciseHandler(request).post(id_)


@app.route("/task/<int:id_>", methods=['GET', 'POST'])
@login_required
def task(id_) -> Union[Response, str]:
    """
    Site to display a single task
    @param id_: The id of the task
    @type id_: int
    @return: The rendered task site
    """
    if request.method == 'GET':
        return TaskHandler(request).get(id_)
    elif request.method == 'POST':
        return TaskHandler(request).post(id_)


@app.route("/tasks")
@login_required
def tasks() -> str:
    """
    Site for a list of all the tasks
    @return: The rendered tasks site
    """
    return TaskListHandler(request).get()


@app.route("/task/add", methods=['GET', 'POST'])
@login_required
def addTask() -> Union[Response, str]:
    """
    Site to add a Task
    @return: Rendered Task site or redirect
    """
    if request.method == 'GET':
        return AddTaskHandler(request).get()
    elif request.method == 'POST':
        return AddTaskHandler(request).post()


@app.route("/task/delete/<int:id_>", methods=['GET', 'POST'])
@login_required
def deleteTask(id_: int) -> Union[Response, str]:
    """
    Deleting a exercise from the database
    @param id_: The identifier of the exercise
    @type id_: int
    @return: Redirect to another view.
    """
    if request.method == 'GET':
        return DeleteTaskHandler(request).get(id_)
    elif request.method == 'POST':
        return DeleteTaskHandler(request).post(id_)


@app.route("/task/<int:id_>/attachment/add", methods=['POST'])
@login_required
def addTaskAttachment(id_: int) -> Union[Response, str]:
    """
    Adding a Attachment File to a Task
    @param id_: The id of the task that we wanna add the attachment to
    @type id_: int
    @return: Redirect to another view
    @rtype: Response/str
    """
    if request.method == 'POST':
        return AddTaskAttachmentHandler(request).post(id_)


@app.route("/task/<int:task_id_>/attachment/<int:attachment_id_>", methods=['GET'])
@login_required
def TaskAttachment(task_id_: int, attachment_id_:int) -> Union[Response, str]:
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


@app.route("/task/<int:task_id_>/attachment/<int:attachment_id_>/delete>", methods=['GET', 'POST'])
@login_required
def deleteTaskAttachment(task_id_: int, attachment_id_:int) -> Union[Response, str]:
    """
    Deleting an Attachment from Task
    @param task_id_: The id of the task
    @type task_id_: int
    @param attachment_id_: The id of the Attachment
    @type attachment_id_: int
    @return: Redirect to another view
    @rtype: Response/str
    """
    if request.method == 'GET':
        return DeleteTaskAttachmentHandler(request).get(task_id_, attachment_id_)

    elif request.method == 'POST':
        return DeleteTaskAttachmentHandler(request).post(task_id_, attachment_id_)


@app.route("/task/<int:id_>/instruction/add", methods=['POST'])
@login_required
def addTaskInstruction(id_: int) -> Union[Response, str]:
    """
    Adding an Instruction File to a Task
    @param id_: The id of the task that we wanna add the Instruction to
    @type id_: int
    @return: Redirect to another view
    @rtype: Response/str
    """
    if request.method == 'POST':
        return AddTaskInstructionHandler(request).post(id_)


@app.route("/task/<int:task_id_>/instruction/<int:instruction_id_>", methods=['GET'])
@login_required
def TaskInstruction(task_id_: int, instruction_id_:int) -> Union[Response, str]:
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


@app.route("/task/<int:task_id_>/instruction/<int:instruction_id_>/delete", methods=['GET', 'POST'])
@login_required
def deleteTaskInstruction(task_id_: int, instruction_id_: int) -> Union[Response, str]:
    """
    Deleting an Instruction from a Task
    @param task_id_: The id of the task
    @type task_id_: int
    @param instruction_id_: The id of the Attachment
    @type instruction_id_: int
    @return: Redirect to another view
    @rtype: Response/str
    """
    if request.method == 'GET':
        return DeleteTaskInstructionHandler(request).get(task_id_, instruction_id_)

    elif request.method == 'POST':
        return DeleteTaskInstructionHandler(request).post(task_id_, instruction_id_)


def admin_frontend():
    http_server = WSGIServer(("0.0.0.0", int(config.adminPort)), app)
    http_server.serve_forever()


if __name__ == "__main__":
    admin_frontend()
    # app.run(port=config.adminPort)
