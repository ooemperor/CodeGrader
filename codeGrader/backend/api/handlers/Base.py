"""
Base Handler for the backend API. Setting basic properties like a session.
@author: mkaiser
"""
from codeGrader.backend.db import Session


class BaseHandler:
    """
    The Class for the Basic Handler of the backend API.
    This Handler will be the parent class for all the other handlers.
    """

    def __init__(self):
        """
        Constructor of the BaseHandler
        Setting up Ojbects and params that we use in all handlers.
        @return: No return
        """
        self.sql_session = Session()  # creating the  session for later use
        self.cls = type(self)

    def create_generic_response(self, method: str, id_: int, response: str): # TODO: move to the ErrorHandlerClass
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
        return out

    def create_generic_error_response(self, method: str, id_: int, error: Exception):
        """
        Generating a generic error response when there is some sort of a Problem.
        @param method: The method used to call the handler e.g. PUT, POST and more
        @type method: str
        @param id_: The id_ of the object if provided
        @type id_: int or None
        @param error: The Exception Object that has gotten raised.
        @return: The custom error message that shall be provided to the user.
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

    def get(self, id_: int):
        """
        Get a specific Object from the database from the corresponding table
        Will be overwritten in some of the subclasses for better assertions and preprocessing
        @param id_: the id of the object in the database
        @type id_: int
        @return: JSON representation of the object
        @rtype: str
        """

        assert (id_ is not None) and (id_ > 0)
        try:
            obj_ = self.sql_session.get_object(self.dbClass, id_)
            assert obj_ is not None
            return obj_.toJson()
        except Exception as err:
            return self.create_generic_error_response('GET', id_, err)

    def post(self, dict_: dict):
        """
        Creating a new user object and writing in the database
        @param dict_: The dictionary/ key:value pair for the creation of the object
        @type dict_: dict
        @return: True else Error # TODO: Add more meaningful return Type
        @rtype: Boolean
        """
        assert dict_ is not None
        assert len(dict_.keys()) >= 0
        try:
            obj_ = self.dbClass(**dict_)
            new_obj_id = self.sql_session.create(obj_)
            return self.create_generic_response('POST', new_obj_id, f"{self.dbClass} has been successfully created")
        except Exception as err:
            return self.create_generic_error_response('POST', new_obj_id, err)



    def put(self, id_: int, dict_: dict):
        """
        Updating a existing Object in the database
        @param id_: The identifier of the object
        @type id_: int
        @param dict_: the arguments for the object that are updated
        @type dict_: key:value pairs
        @return: True or False depending on the outcome of the post. # TODO: will be further refined
        @rtype: Boolean
        """
        assert (id_ is not None) and (id_ > 0)
        assert dict_ is not None
        assert len(dict_.keys()) > 0
        try:
            self.sql_session.update(self.dbClass, id_, dict_)
            return self.create_generic_response('PUT', id_, f"{self.dbClass} has been successfully updated")
        except Exception as err:
            return self.create_generic_error_response('PUT', id_, err)


    def delete(self, id_: int):
        """
        Deleting a object from the database
        @param id_: The identifier of the object
        @type id_: int
        @return: True or False depending on the outcome of the post. # TODO: will be further refined
        @rtype: Boolean
        """
        assert (id_ is not None) and (id_ > 0)
        try:
            self.sql_session.delete(self.dbClass, id_)
            return self.create_generic_response('DELETE', id_, f"{self.dbClass} has been successfully deleted")
        except Exception as err:
            return self.create_generic_error_response('DELETE', id_, err)
