"""
Holds all kind of functionality used by the frontend that needs to implement functionality with apis
@author: mkaiser
"""

from codeGrader.frontend.config import config
import requests


class ApiHandler():
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

        self.url = api_url
        self.authentication_type = authentication_type
        self.authentication_token = authentication_token

    def _make_request(self, method: str, path: str, body: str = None):
        """
        Make an Api Request on the given path with the given
        @param method: The Method to use in the api
        @type method: str
        @param path: The path of the api that shall be used
        @type path: str
        @param body: The body of the request that shall be made
        @type body: str / dict
        @return: Formatted response of the api.
        @rtype:
        """
        path = f"{self.url}{path}"
        headers = dict()
        if self.authentication_type is None:
            headers["Authorization"] = f"{self.authentication_type} {self.authentication_token}"

        if method == 'GET':
            assert body is None
            response = requests.get(path, headers=headers)

        elif method == 'POST':
            assert body is not  None
            response = requests.post(path, headers=headers, json=body)

        elif method == 'PUT':
            assert body is not None
            response = requests.put(path, headers=headers, json=body)

        elif method == 'DELETE':
            assert body is None
            response = requests.delete(path, headers=headers)
        else:
            raise TypeError("Method not allowed! Allowed are: DELETE, GET, POST, PUT")

        return response

    def get(self, path: str):
        """
        use GET Method on the API
        @param path: the path on which to call the request
        @return:
        """
        response = self._make_request('GET', path)
        assert response.response_code == 200
        assert response.text is not None

        return response.text

    def post(self, path: str, body: str = None):
        """
        use POST method on the API
        @param path: the path on which to call the request
        @param body: The body taht shall be attached to the request
        @return: The response of the API
        """
        assert body is not None
        response = self._make_request('POST', path, body)

        assert (response.status_code == 200 or response.status_code == 201)
        assert response.text is not None

        return response.text

    def put(self, path: str, body: str = None):
        """
        use PUT method on the API
        @param path: the path on which to call the request
        @param body: The body taht shall be attached to the request
        @return: The response of the API
        """
        assert body is not None

        response = self._make_request('PUT', path, body)

        assert (response.status_code == 200 or response.status_code == 204)
        assert response.text is not None

        return response.text

    def delete(self, path: str):
        """
        use DELETE Method on the API
        @param path: the path on which to call the request
        @return: The response of the API
        """
        response = self._make_request('DELETE', path)

        assert response.status_code == 200
        assert response.text is not None

        return response.text
