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
Script File for starting the User Frontend
@author: mkaiser
"""

import sys
import os
import subprocess

def main():
    """
    Starting a new instance of the EvaluationService
    @return:
    """
    os.chdir("/usr/local/lib/python3.11/dist-packages/codeGrader/frontend/user")
    os.system("python3 app.py)


if __name__ == '__main__':
    sys.exit(main())
