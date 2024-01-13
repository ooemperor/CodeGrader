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