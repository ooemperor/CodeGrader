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
File for the ResponseHandlers.
e.g. GenericResponseHandler and ErrorResponse Handler
@author: mkaiser
"""
import sqlalchemy.orm.exc
from .Exceptions import AuthorizationException


class GenericResponseHandler:
    """
    Handler for generic responses. e.g. no exception has been raised
    """

    def __init__(self):
        """
        empty constructor for the Generic ResponseHandler
        """

    @staticmethod
    def _get_response_code(method: str) -> int:
        """
        Calculating the resonse code for a specific method
        @param method: The method used on the API Call
        @type method: str
        @return: The response code
        @rtype: int
        """
        if method == 'POST':
            return 201
        elif method == 'DELETE':
            return 204
        else:
            return 200

    def generate_response(self, method: str, response: str, id_: int = None, **kwargs) -> (dict, int):
        """
        Generates a generic method for a response Body
        @param method: the request method
        @type method: String
        @param id_: The identifier used in the operation
        @type id_: int
        @param response: The response message that should be added
        @type: response: String
        @return: The response JSON
        @rtype: (dict, int)
        """
        out = dict()
        _response = dict()
        _response["id"] = id_
        _response["message"] = response
        out["method"] = method
        out["response"] = _response

        for key, value in kwargs.items():  # adding custom arguments to the response message
            out[key] = value

        return out, self._get_response_code(method)


class ErrorResponseHandler:
    """
    ErrorHandler Class.
    This Handler will return a properly rendered error message based on the Error that occurred in the handler classes.
    """

    def __init__(self):
        """
        Constructor for the Errorhandler
        """

    @staticmethod
    def _get_response_code(exception: Exception) -> int:
        """
        Calculating the response code for an exception
        @param exception: The exception that has been raised
        @type exception: str
        @return: the response code according to the error
        @rtype: int
        """
        if exception in [sqlalchemy.orm.exc.UnmappedInstanceError]:
            # object was not found in the database
            return 404
        elif issubclass(type(exception), AuthorizationException):
            return 401
        else:
            # return general server error
            return 500

    def generate_response(self, method: str, exception: Exception, id_: int = None) -> (dict, int):
        """
        The Response Generator
        @param method: The method of the request
        @type method: str
        @param id_: The id_ of an object that we wanted to operate on.
        @type id_: int
        @param exception: The exception that has been raised while handling the request.
        @type exception: Exception
        @return: The properly rendered repsonse
        @rtype: (dict, int)
        """

        out = dict()

        error_out = dict()
        error_out["error_type"] = str(type(exception))
        error_out["error_msg"] = str(exception)

        _response = dict()
        if id_ is not None:
            _response["id"] = id_
        _response["error"] = error_out

        out["method"] = method
        out["response"] = _response
        return out, self._get_response_code(exception)
