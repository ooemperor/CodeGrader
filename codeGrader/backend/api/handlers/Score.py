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
File that contains all methods and classes about the score calculation and filtering
@author: mkaiser
"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import Task, Exercise, Subject, User
from codeGrader.backend.config import config
import urllib


class ScoreHandler(BaseHandler):
    """
    Handler Class for the preprocessing of all the scores.
    """

    def __init__(self) -> None:
        """
        Constructor for the ScoreHandler
        """
        super().__init__()
        self.dbClass = None  # will be set later as needed.

    def get_scores(self, view: str, arguments: dict = {}):
        """
        Preprocessing and calcualtion function for the score rendering
        What to render is defined by the view parameter (e.g. Subject, Exercise, Task)
        The arguments that are supported in the filtering are object_id and user_id
        Object_id will be used for task, exercise and subject, according to which view type is set
        @param view: Which view shall be rendered
        @type view:
        @param arguments: The arguments provided in the API Call as URL arguments
        @type arguments: str
        @return: Response Dictionary with all the objects
        @rtype: dict
        """
        if view not in ["subject", "exercise", "task"]:
            # the view is not allowed so we return a error message
            return self.create_generic_error_response('GET', ValueError(
                "The type of view that has been provided is not valid!"))

        if view == 'task':
            self.dbClass = Task

        elif view == 'exercise':
            self.dbClass = Exercise

        elif view == 'subject':
            self.dbClass = Subject

        else:
            # it should be impossible to get in here, so we throw an error if we manage to get in here
            raise ValueError(
                "The view type that has been provided is not allowed and has not been caught before. Please Contanct your administrator")

        # the dbClass attribute is set at this point, continue with the query
        output = dict()  # the dictionary in which we will insert all the data at the end
        object_list = []
        output_data_list = []  # temporary list holding all the values for a single object instance
        if "user_id" in arguments.keys():
            # we do only want to filter for one specific user
            user_id = urllib.parse.unquote(arguments.get("user_id"))
            user_id = int(user_id)

            if "object_id" in arguments.keys():
                # since the object_id is set, we do just need to filter for one object.
                object_id = urllib.parse.unquote(arguments.get("object_id"))
                db_object = self.sql_session.get_object(self.dbClass, object_id)
                print(db_object.id)
                score = db_object.user_score(user_id)

                user_data_dict = {"user_id": user_id, "score": score}
                output_data_list.append(user_data_dict)

                output[str(self.dbClass.__table__)] = [{object_id: output_data_list}]

            else:
                # the object_id is not given, so we need to query all objects
                db_objects = self.sql_session.get_all(self.dbClass)
                for db_object in db_objects:
                    score = db_object.user_score(user_id)
                    print(score)
                    user_data_dict = {"user_id": user_id, "score": score}
                    object_list.append({db_object.id: user_data_dict})

                output[str(self.dbClass.__table__)] = object_list

        else:
            # the user_id has not been provided, so we need to query all users
            users = self.sql_session.get_all(User)

            if "object_id" in arguments.keys():
                # since the object_id is set, we do just need to filter for one object.
                object_id = urllib.parse.unquote(arguments.get("object_id"))
                db_object = self.sql_session.get_object(self.dbClass, object_id)

                for user in users:
                    score = db_object.user_score(user.id)
                    user_data_dict = {"user_id": user.id, "score": score}
                    output_data_list.append(user_data_dict)
                object_list.append({object_id: output_data_list})

                output[str(self.dbClass.__table__)] = object_list

            else:
                # no object_id has been provided and no user_id has been provided so we need to query everything
                db_objects = self.sql_session.get_all(self.dbClass)
                for db_object in db_objects:
                    for user in users:
                        score = db_object.user_score(user.id)
                        user_data_dict = {"user_id": user.id, "score": score}
                        output_data_list.append(user_data_dict)
                    object_list.append({db_object.id: output_data_list})
                    output_data_list = []

                output[str(self.dbClass.__table__)] = object_list

        # rendering of one of the four cases has finished so we return it.
        return output
