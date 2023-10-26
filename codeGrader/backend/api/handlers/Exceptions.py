"""
Contains all the custom written Exceptions used in the handlers for the business logic and more
@author: mkaiser
"""


class AuthorizationFail(Exception):
    """
    The Authorization via Bearer Token was not successful
    """

class AuthorizationRequired(Exception):
    """
    No Authorization has been provided but is needed.
    """