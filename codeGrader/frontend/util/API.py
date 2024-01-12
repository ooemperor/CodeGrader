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
Holds all kind of functionality used by the frontend that needs to implement functionality with apis
@author: mkaiser
"""

import json
from codeGrader.frontend.config import config
import requests
from requests import Response
from typing import Union


class ApiHandler:
    """
    Handler for a API
    Calls and makes calls to a specific api handling authentication and more
    """

    def __init__(self, api_url: str, authentication_type: str = None, authentication_token: str = None):
        """
        Constructor for the ApiHandler
        @param api_url: The URL to the api to make the calls to.
        @type api_url: str
        @param authentication_type: The type of authentication that is used by the api:
        @type authentication_type: str
        @param authentication_token: Authentication Token for the api Default is None
        @type authentication_token: str
        """
        self.debug = False  # parameter if the output from the api shall be printed or not
        self.url = api_url
        self.authentication_type = authentication_type
        self.authentication_token = authentication_token

    def _make_request(self, method: str, path: str, body: str = None, data: str = None, files: str = None) -> Response:
        """
        Make an Api Request on the given path with the given
        @param method: The Method to use in the api
        @type method: str
        @param path: The path of the api that shall be used
        @type path: str
        @param body: The body of the request that shall be made
        @type body: str / dict
        @param data: The data of the request that shall be made
        @type data: str / dict
        @param files: The files of the request that shall be made
        @type files: str / dict
        @return: Formatted response of the api.
        @rtype:
        """
        path = f"{self.url}{path}"
        headers = dict()
        if self.authentication_type is not None:
            headers["Authorization"] = f"{self.authentication_type} {self.authentication_token}"

        if method == 'GET':
            assert body is None
            response = requests.get(path, headers=headers)

        elif method == 'POST':
            assert body is not None or data is not None or files is not None
            response = requests.post(path, headers=headers, json=body, data=data, files=files)

        elif method == 'PUT':
            assert body is not None
            response = requests.put(path, headers=headers, json=body, data=data, files=files)

        elif method == 'DELETE':
            assert body is None
            response = requests.delete(path, headers=headers)
        else:
            raise TypeError("Method not allowed! Allowed are: DELETE, GET, POST, PUT")

        return response

    @staticmethod
    def _cast_dict(dictionary: str) -> Union[str, dict]:
        """
        Try casting an string to a Dictionary
        @param dictionary: The string that shall be casted to a dictionary
        @type dictionary: str
        @return: The dictionary or the orginal string
        @rtype: dict or str
        """
        try:
            return json.loads(dictionary)

        except json.JSONDecodeError as err:
            return dictionary

    @staticmethod
    def _construct_filter(path: str, **kwargs) -> str:
        """
        Constructing the filter criterias by appending them to the string.
        @param path: The base path of the url call
        @type path: str
        @param kwargs: The arguments that we wanna append to the url as filter
        @type kwargs: key-value pairs
        @return: The newly created path string with the appended filter criterias
        @rtype: str
        """
        # appending ? to the path to indicate the start of filters
        path += "?"

        if kwargs is not None:  # only try to append if there is something in kwargs
            for key, value in kwargs.items():
                if value in ["", None]:
                    continue  # do not append the filter string since it is empty

                path += f"{str(key)}={str(value)}&"  # appending kwargs to the base path

        return path

    def get(self, path: str, **kwargs) -> Union[str, dict]:
        """
        use GET Method on the API
        @param path: the path on which to call the request
        @type path: str
        @return: The response text of the API response
        @rtype: str
        """
        path = self._construct_filter(path, **kwargs)
        response = self._make_request('GET', path)
        assert response.status_code == 200
        assert response.text is not None

        return self._cast_dict(response.text)

    def post(self, path: str, body: Union[str, dict] = None, data: Union[str, dict] = None,
             files: Union[str, dict] = None) -> dict:
        """
        use POST method on the API
        @param path: the path on which to call the request
        @type path: str
        @param body: The body taht shall be attached to the request
        @type body: str
        @param data: The data that shall be attached to the request, used when we wanna transfer data body and files
        @type data: str
        @param files: The files that shall be attached to the request
        @type files: str
        @return: The response text of the API response
        @rtype: str
        """
        assert body is not None or data is not None or files is not None
        response = self._make_request('POST', path, body, data, files)
        if self.debug:
            print(self._cast_dict(response.text))
        assert (response.status_code == 200 or response.status_code == 201)
        assert response.text is not None

        return self._cast_dict(response.text)

    def put(self, path: str, body: Union[str, dict] = None, data: Union[str, dict] = None,
            files: Union[str, dict] = None) -> dict:
        """
        use PUT method on the API
        @param path: the path on which to call the request
        @type path: str
        @param body: The body that shall be attached to the request
        @type body: str
        @param data: The data that shall be attached to the request, used when we wanna transfer data body and files
        @type data: str
        @param files: The files that shall be attached to the request
        @type files: str
        @return: The response text of the API response
        @rtype: dict
        """
        assert body is not None

        response = self._make_request('PUT', path, body, data, files)
        if self.debug:
            print(self._cast_dict(response.text))
        assert (response.status_code == 200 or response.status_code == 204)
        assert response.text is not None

        return self._cast_dict(response.text)

    def delete(self, path: str) -> dict:
        """
        use DELETE Method on the API
        @param path: the path on which to call the request
        @type path: str
        @return: The response text of the API response
        @rtype: dict
        """
        response = self._make_request('DELETE', path)
        if self.debug:
            print(self._cast_dict(response.text))
        assert response.status_code == 200 or response.status_code == 204
        assert response.text is not None

        return self._cast_dict(response.text)

    def get_file(self, path: str, **kwargs) -> Response:
        """
        use GET Method on the API specifically to download files
        @param path: the path on which to call the request
        @type path: str
        @return: The response text of the API response
        @rtype: str
        """
        path = self._construct_filter(path, **kwargs)
        response = self._make_request('GET', path)
        assert response.status_code == 200
        assert response.text is not None

        return response
