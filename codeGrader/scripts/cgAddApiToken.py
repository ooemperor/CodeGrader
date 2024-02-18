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
Script to generate an api token in the backend for the frontend.
Script will be generated and added to the server path.
@author: mkaiser
"""

from codeGrader.backend.db import Session, APIToken
import argparse
import sys


def add_token(description):
    """
    Generate a API Token for the backend api, create the object in the database
    Return the token itself in a print statement
    @param description: The description for the token
    @type description: str
    @return: Authentication Token
    @rtype: str
    """

    sql = Session()  # open session
    api_token = APIToken(description=description)  # create the object
    token = api_token.token  # read the token from the object
    sql.create(api_token)  # write token to sql

    print(token)


def main():
    """
    Parsing the description argument via a ArgumentParser and creating the user in the database
    """
    parser = argparse.ArgumentParser(
        description="Add API Key to the Database"
    )
    parser.add_argument('-d', '--description')

    args = parser.parse_args()
    add_token(args.description)


if __name__ == '__main__':

    sys.exit(main())
