"""
File for the ErrorHanlderclass.
@author: mkaiser
"""


class ErrorHandler:
    """
    # TODO: Create the error Handler
    ErrorHandler Class.
    This Handler will return a properly rendered error message based on the Error that occurred in the handler classes.
    """

    def __init__(self):
        """
        Constructor for the Errorhandler
        """

    def generate_response(self, method: str, exception: Exception):
        """
        The Response Generator
        @param exception: The exception that has been raised while handling the request.
        @type exception: Exception
        @param method: The method of the request
        @type method: str
        @return: The properly rendered repsonse
        @rtype: dict
        """

        out = dict()

        error_out = dict()
        error_out["error_type"] = str(type(error))
        error_out["error_msg"] = str(error)

        _response = dict()
        _response["id"] = id_
        _response["error"] = error_out

        out["method"] = method
        out["response"] = _response
        return out