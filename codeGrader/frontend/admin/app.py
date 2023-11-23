"""
Route definition and main File for the Admin Frontend of the CodeGrader
@author: mkaiser
@version: 1.0
"""
from flask import Flask, request, render_template, url_for, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from codeGrader.frontend.config import config
from codeGrader.frontend.admin import templates
from codeGrader.frontend.admin.handlers import AdminUserLoginHandler, AdminUserSessionHandler, SessionAdminUser, \
    UserListHandler, UserHandler, HomeHandler, AdminUserListHandler, AdminUserHandler, ProfileListHandler, \
    ProfileHandler, SubjectListHandler, SubjectHandler, TaskHandler, TaskListHandler, ExerciseHandler, \
    ExerciseListHandler, AddAdminUserHandler, AddProfileHandler, AddUserHandler

app = Flask(config.adminAppName, template_folder=templates.__path__[0])

# configuration of the login_manager and attaching it to the app
app.secret_key = config.adminSecretKey
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def adminUser_login(adminUser_id):
    """
    User load of the login_manager
    Returns the frontend represenation of the user
    @param adminUser_id: the id of the user
    @type adminUser_id: int
    @return: The frontend User Object
    @rtype: SessionAdminUser
    """
    user = SessionAdminUser(adminUser_id)
    return user


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
        user_id = AdminUserLoginHandler(request).post()
        if user_id:
            user = adminUser_login(user_id)
            login_user(user)
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


@login_manager.unauthorized_handler
def unauthorized():
    """
    Returns to login page if you are not properly logged in
    @return: Redirection to the login site.
    """
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    """
    The Home site of the admin frontend
    @return: Rendered Home Template
    """
    return HomeHandler(request).get()


@app.route("/user/<int:id_>", methods=['GET', 'POST'])
@login_required
def user(id_):
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
def users():
    """
    Site to display all users
    @return: Rendered Users Site
    """
    return UserListHandler(request).get()


@app.route("/addUser", methods=['GET', 'POST'])
@login_required
def addUser():
    """
    Site to add an User
    @return: Rendered Users site or redirect
    """
    if request.method == 'GET':
        return AddUserHandler(request).get()
    elif request.method == 'POST':
        return AddUserHandler(request).post()


@app.route("/adminUser/<int:id_>", methods=['GET', 'POST'])
@login_required
def adminUser(id_):
    """
    @param id_: The identifier of the adminuser
    @type id_: int
    @return: The rendered adminUser
    """
    if request.method == 'GET':
        return AdminUserHandler(request).get(id_)
    elif request.method == 'POST':
        return AdminUserHandler(request).post(id_)


@app.route("/adminUsers")
@login_required
def adminUsers():
    """
    Site to display all Admins
    @return: Rendered AdminUsers Site
    """
    return AdminUserListHandler(request).get()


@app.route("/addAdminUser", methods=['GET', 'POST'])
@login_required
def addAdminUser():
    """
    Site to add an Admin User
    @return: Rendered Admin Users site or redirect
    """
    if request.method == 'GET':
        return AddAdminUserHandler(request).get()
    elif request.method == 'POST':
        return AddAdminUserHandler(request).post()



@app.route("/profile/<int:id_>", methods=['GET', 'POST'])
@login_required
def profile(id_):
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
def profiles():
    """
    Site for a list of all the profiles
    @return: The rendered Profiles site
    """
    return ProfileListHandler(request).get()


@app.route("/addProfile", methods=['GET', 'POST'])
@login_required
def addProfile():
    """
    Site to add a Profile
    @return: Rendered Profile site or redirect
    """
    if request.method == 'GET':
        return AddProfileHandler(request).get()
    elif request.method == 'POST':
        return AddProfileHandler(request).post()


@app.route("/subject/<int:id_>", methods=['GET', 'POST'])
@login_required
def subject(id_):
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
def subjects():
    """
    Site for a list of all the subjects
    @return: The rendered Subjects site
    """
    return SubjectListHandler(request).get()


@app.route("/exercise/<int:id_>", methods=['GET', 'POST'])
@login_required
def exercise(id_):
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
def exercises():
    """
    Site for a list of all the exercises
    @return: The rendered exercises site
    """
    return ExerciseListHandler(request).get()


@app.route("/task/<int:id_>", methods=['GET', 'POST'])
@login_required
def task(id_):
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
def tasks():
    """
    Site for a list of all the tasks
    @return: The rendered tasks site
    """
    return TaskListHandler(request).get()


if __name__ == "__main__":
    app.run(port=config.adminPort)
