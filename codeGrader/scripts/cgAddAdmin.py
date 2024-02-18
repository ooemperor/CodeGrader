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
Script to create an admin user object in the Database for login in the admin frontend
Script will be generated and added to the server path.
@author: mkaiser
"""

from codeGrader.backend.db import Session, AdminUser
import argparse
import sys


def addAdmin(username, first_name, last_name, email, password):
    """
    Generate an admin user that will be added to the database for the initial setups
    @param username: The username for the new admin
    @type username: str
    @param first_name: The first name of the new admin
    @type first_name: str
    @param last_name: The lastname of the new admin
    @type last_name: str
    @param email: The email of the new admin
    @type email: str
    @param password: The password of the new admin
    @type password: str
    @return: Print statement about the user
    @rtype: str
    """
    sql = Session()  # open session
    admin_dict = {
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "tag": ""
    }
    admin_user = AdminUser(**admin_dict)  # create the object
    sql.create(admin_user)  # write token to sql

    print(f"User {username} has been created with password {password}")


def main():
    """
    The main method adding an admin to the backend.
    @return:
    """

    parser = argparse.ArgumentParser(
        description="Add Admin User to the Database"
    )
    parser.add_argument('-u', '--username')
    parser.add_argument('-fn', '--first_name')
    parser.add_argument('-ln', '--last_name')
    parser.add_argument('-e', '--email')
    parser.add_argument('-p', '--password')

    args = parser.parse_args()

    addAdmin(args.username, args.first_name, args.last_name, args.email, args.password)


if __name__ == '__main__':
    sys.exit(main())
