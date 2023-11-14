"""
Route definition and main File for the Admin Frontend of the CodeGrader
@author: mkaiser
@version: 1.0
"""
import io
import os
import mimetypes
from functools import wraps

from flask import Flask, request, render_template, url_for, redirect
from flask_login import LoginManager
from codeGrader.frontend.config import config
from codeGrader.frontend.admin import templates

app = Flask(config.adminAppName, template_folder=templates.__path__[0])

login_manager = LoginManager()


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")



if __name__ == "__main__":
    app.run(port=config.adminPort)
