"""
Route defintion of the User Frontend of the CodeGrader
@author: mkaiser
@version: 1.0
"""

import flask_login
from flask import Flask, request, render_template, url_for, redirect, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user
from codeGrader.frontend.config import config
from codeGrader.frontend.user import templates
from codeGrader.frontend.user.handlers import UserSessionHandler, SessionUser, UserLoginHandler, HomeHandler

app = Flask(config.adminAppName, template_folder=templates.__path__[0])

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


if __name__ == "__main__":
    app.run(port=config.userPort)
