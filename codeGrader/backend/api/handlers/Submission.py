"""
Holds the Handlers for everything that corresponds with the Submission Class.
@author: mkaiser
"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import Submission


class SubmissionHandler(BaseHandler):
    """
    Handler for the Submission Class.
    Using the default get, post, delete and put methods defined in the BaseHandler
    @see: BaseHandler
    """
    def __init__(self):
        """
        Constructor for the ProfileHandler
        """
        super().__init__()
        self.dbClass = Submission

    def post(self, dict_: dict):
        """
        Creating a new user object and writing in the database
        Overwrites the function used in the BaseHandler
        @param dict_: The dictionary/ key:value pair for the creation of the object
        @type dict_: dict
        @return: Dictionary Containing the error or the response data
        @rtype: dict
        """
        assert dict_ is not None
        assert len(dict_.keys()) >= 0
        new_obj_id = None
        try:
            obj_ = self.dbClass(**dict_)
            new_obj_id = self.sql_session.create(obj_)
            return self.create_generic_response('POST', f"{self.dbClass} has been successfully created", new_obj_id)
        except Exception as err:
            return self.create_generic_error_response('POST', err, new_obj_id)

    def _startExecution(self):

