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
Base Handler for the backend API. Setting basic properties like a session.
@author: mkaiser
"""
import sqlalchemy.orm.decl_api

from codeGrader.backend.db import Session
from .ResponseGenerator import ErrorResponseHandler, GenericResponseHandler
import urllib
import json


class BaseHandler:
    """
    The Class for the Basic Handler of the backend API.
    This Handler will be the parent class for all the other handlers.
    """
    # definition of non-present instance variable in the parent class
    # these variables will be defined in the child classes
    dbClass: sqlalchemy.orm.decl_api.DeclarativeMeta

    def __init__(self):
        """
        Constructor of the BaseHandler
        Setting up Objects and params that we use in all handlers.
        @return: No return
        """
        self.sql_session = Session()  # creating the  session for later use
        self.cls = type(self)
        self.errorResponseHandler = ErrorResponseHandler()  # adding errorhandler in case we need it
        self.genericResponseHandler = GenericResponseHandler()  # generic Response Handler when there are no errors

    def create_generic_response(self, method: str, response: str, id_: int = None):
        """
        Generates a generic method for a response Body
        @param method: the request method
        @type method: String
        @param response: The response message that should be added
        @type: response: String
        @param id_: The identifier used in the operation
        @type id_: int
        @return: The response JSON
        @rtype: dict
        """
        return self.genericResponseHandler.generate_response(method, response, id_)

    def create_generic_error_response(self, method: str, exception: Exception, id_: int = None):
        """
        Generating a generic error response when there is some sort of a Problem.
        @param method: The method used to call the handler e.g. PUT, POST and more
        @type method: str
        @param exception: The Exception Object that has gotten raised.
        @type exception: Exception
        @param id_: The id_ of the object if provided
        @type id_: int or None
        @return: The custom error message that shall be provided to the user.
        @rtype: dict
        """
        return self.errorResponseHandler.generate_response(method, exception, id_)

    def _preprocess_data_dict(self, dict_: dict):
        """
        Makes a preprocessing on the dict_ provided for post and put methods.
        This method will be overwritten in the child classes to adapt for special use cases.
        @param dict_: The data dictionary with the object data for put and post
        @type dict_: dict
        @return: The preprocessed data dict_
        @rtype: dict
        """
        # in the base method we do not do any preprocessing
        # this allows to overwrite the method in child classes
        return dict_

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
            return self.create_generic_error_response('GET', err, id_)

    def post(self, dict_: dict):
        """
        Creating a new object and writing in the database
        @param dict_: The dictionary/ key:value pair for the creation of the object
        @type dict_: dict
        @return: Dictionary Containing the error or the response data
        @rtype: dict
        """
        assert dict_ is not None
        assert len(dict_.keys()) >= 0
        dict_ = self._preprocess_data_dict(dict_)
        new_obj_id = None
        try:
            obj_ = self.dbClass(**dict_)
            new_obj_id = self.sql_session.create(obj_)
            return self.create_generic_response('POST', f"{self.dbClass} has been successfully created", new_obj_id)
        except Exception as err:
            return self.create_generic_error_response('POST', err, new_obj_id)

    def put(self, id_: int, dict_: dict):
        """
        Updating an existing Object in the database
        @param id_: The identifier of the object
        @type id_: int
        @param dict_: the arguments for the object that are updated
        @type dict_: key:value pairs
        @return: Dictionary Containing the error or the response data
        @rtype: dict
        """
        assert (id_ is not None) and (id_ > 0)
        assert dict_ is not None
        assert len(dict_.keys()) > 0
        dict_ = self._preprocess_data_dict(dict_)
        try:
            self.sql_session.update(self.dbClass, id_, dict_)
            return self.create_generic_response('PUT', f"{self.dbClass} has been successfully updated", id_)
        except Exception as err:
            return self.create_generic_error_response('PUT', err, id_)

    def delete(self, id_: int):
        """
        Deleting a object from the database
        @param id_: The identifier of the object
        @type id_: int
        @return: Dictionary Containing the error or the response data
        @rtype: dict
        """
        assert (id_ is not None) and (id_ > 0)
        try:
            self.sql_session.delete(self.dbClass, id_)
            return self.create_generic_response('DELETE', f"{self.dbClass} has been successfully deleted", id_)
        except Exception as err:
            return self.create_generic_error_response('DELETE', err, id_)

    def get_all(self, arguments: dict={}) -> dict:
        """
        Get all objects of a Class.
        @param arguments: The arguments provided in the API Call as URL arguments
        @type arguments: str
        @return: Response Dictionary with all the objects
        @rtype: dict
        """
        if arguments is None:
            arguments = dict()
        try:
            # reading the objects out of the database
            objects = self.sql_session.get_all(self.dbClass)

            if len(objects) == 0:  # no data found
                return self.create_generic_response('GET', f"No Objects entries to display")

            else:
                object_list = []

                for object_ in objects:
                    object_dict = object_.toJson()

                    if len(arguments.keys()) == 0:  # no filtering provided
                        object_list.append(object_dict)
                        continue

                    insert_candidate = True
                    for key in arguments.keys():  # filtering with the provided filter arguments

                        if str(object_dict[key]) != urllib.parse.unquote(arguments.get(key)):  # compare the values
                            insert_candidate = False  # if they do not match, the object is no longer a candidate for insert
                            break

                    if insert_candidate is True:
                        object_list.append(object_dict)

                output = dict()
                output[str(self.dbClass.__table__)] = object_list
                return output
        except Exception as err:
            return self.create_generic_error_response('GET', err)
