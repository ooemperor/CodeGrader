"""
Route definition and main File that runs the application.
@author: mkaiser
@version: 1.0
"""

from flask import Flask, request

from config import config



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
    # TODO: remove home directory after paths are impelentet.

# TODO: Add all the routes needed for the backend API


# starting the web application
app.run(port=config.port, debug=config.debug)
