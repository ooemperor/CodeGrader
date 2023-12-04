"""
All the needed authentication for the api
@author: mkaiser
"""

from codeGrader.backend.db import Session, APIToken
from codeGrader.backend.config import config
from .ResponseGenerator import ErrorResponseHandler
from .Exceptions import AuthorizationFail, AuthorizationRequired
from functools import wraps
import sqlalchemy.exc
from sqlalchemy import select
from flask import request


def _check_authentication(api_token: str) -> None:
    """
    Checking if the provided api_token is valid
    @param api_token: The Bearer Token used in the authentication.
    @type api_token: str
    @return:
    """
    sql = Session()

    with sql.session.begin() as session:
        try:
            session.scalars(select(APIToken).where(APIToken.token == api_token)).one()
        except sqlalchemy.exc.NoResultFound as error:
            # we did not find any object with the given api key in the database on the correct able.
            raise


def authentication(f):
    """
    Decorator Function for the authentication
    @param f: The automatically passed function f
    @type f: function
    @return: The decorated function
    @rtype: function
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        if config.tokenAuthorization:
            if "Authorization" in request.headers:

                try:
                    _check_authentication(request.headers['Authorization'].split(' ')[1])
                    return f(*args, **kwargs)

                except sqlalchemy.exc.NoResultFound:
                    error = AuthorizationFail("API Key is not valid")
                    return ErrorResponseHandler().generate_response(request.method, error)

            else:
                error = AuthorizationRequired("No Authorization has been provided")
                return ErrorResponseHandler().generate_response(request.method, error)

        else:
            return f(*args, **kwargs)
    return decorator
