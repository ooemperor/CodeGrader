"""
Contains all the custom written Exceptions used in the handlers for the business logic and more
@author: mkaiser
"""


class AuthorizationException(Exception):
    """
    Basic AuthorizationException Class
    """


class AuthorizationFail(AuthorizationException):
    """
    The Authorization via Bearer Token was not successful
    """


class AuthorizationRequired(AuthorizationException):
    """
    No Authorization has been provided but is needed.
    """


class AuthorizationTokenExpired(AuthorizationException):
    """
    The Authorization Token is no longer valid. It is past its max valid date
    """