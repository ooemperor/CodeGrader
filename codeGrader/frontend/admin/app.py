"""
Route definition and main File for the Admin Frontend of the CodeGrader
@author: mkaiser
@version: 1.0
"""
import io
import os
import mimetypes
from functools import wraps

from flask import Flask, request, render_template
from codeGrader.frontend.config import config

templatesDir = os.path.abspath('./templates')
app = Flask("3DBoK", template_folder=templatesDir)
app = Flask(config.adminAppName)


@app.route("/")
def home():
    return render_template("base.html")


@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(port=config.adminPort)
