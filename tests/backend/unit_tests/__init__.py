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
Init file for all unit_tests for the tests root folder
Imports all the classes in this directory
@author: mkaiser
"""

from . import test_Task, test_User, test_Profile, test_Subject, test_Exercise, test_Submission, test_APIToken, test_File

__all__ = [test_Task, test_User, test_Profile, test_Subject, test_Exercise, test_Submission, test_APIToken, test_File]
