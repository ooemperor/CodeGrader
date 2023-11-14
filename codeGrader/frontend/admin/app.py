"""
Route definition and main File for the Admin Frontend of the CodeGrader
@author: mkaiser
@version: 1.0
"""
from flask import Flask, request, render_template, url_for, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from codeGrader.frontend.config import config
from codeGrader.frontend.admin import templates
from codeGrader.frontend.admin.handlers import AdminUserLoginHandler, AdminUserHandler, SessionAdminUser


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


@app.route("/")
@login_required
def home():
    """
    The Home site of the admin frontend
    @return: Rendered Home Template
    """
    return render_template("base.html")


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





if __name__ == "__main__":
    app.run(port=config.adminPort)
