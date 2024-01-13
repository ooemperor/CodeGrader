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
