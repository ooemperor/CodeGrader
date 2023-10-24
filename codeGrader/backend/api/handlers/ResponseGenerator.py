"""
File for the ResponseHandlers.
e.g. GenericResponseHandler and ErrorResponse Handler
@author: mkaiser
"""
import sqlalchemy.orm.exc


class GenericResponseHandler:
    """
    Handler for generic responses. e.g. no exception has been raised
    """

    def __init__(self):
        """
        empty constructor for the Generic ResponseHandler
        """

    @staticmethod
    def _get_response_code(method: str):
        if method == 'POST':
            return 201
        elif method == 'DELETE':
            return 204
        else:
            return 200

    def generate_response(self, method: str, id_: int, response: str):
        """
        Generates a generic method for a response Body
        @param method: the request method
        @type method: String
        @param id_: The identifier used in the operation
        @type id_: int
        @param response: The response message that should be added
        @type: response: String
        @return: The response JSON
        @rtype: dict
        """
        out = dict()
        _response = dict()
        _response["id"] = id_
        _response["message"] = response
        out["method"] = method
        out["response"] = _response

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
    def _get_response_code(exception: Exception):
        if exception in [sqlalchemy.orm.exc.UnmappedInstanceError]:
            # object was not found in the database
            return 404
        else:
            # return general server error
            return 500

    def generate_response(self, method: str, id_: int, exception: Exception):
        """
        The Response Generator
        @param method: The method of the request
        @type method: str
        @param id_: The id_ of an object that we wanted to operate on.
        @type id_: int
        @param exception: The exception that has been raised while handling the request.
        @type exception: Exception
        @return: The properly rendered repsonse
        @rtype: dict
        """

        out = dict()

        error_out = dict()
        error_out["error_type"] = str(type(exception))
        error_out["error_msg"] = str(exception)

        _response = dict()
        _response["id"] = id_
        _response["error"] = error_out

        out["method"] = method
        out["response"] = _response
        return out, self._get_response_code(exception)