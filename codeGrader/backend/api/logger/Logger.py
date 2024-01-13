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
Defining the logger class for the codeGrader
Writing the own logger class for better control of the logged messages.

@author: mkaiser
"""

from datetime import datetime as dt
from codeGrader.backend.config import config


class Logger:
    """
    Class for our logger that is used in the project.
    """

    def __init__(self):
        """
        Constructor of the logger
        @return: No Return from the Constructor
        """

        self.debug = config.debug
        self.writeToFile = False

    def info(self, message: str):
        """
        General Information to be logged.
        General Information e.g. User has opened something.
        @param message: The message that we shall display
        @type message: str
        @return: True if successful
        @rtype: Boolean
        """
        self._write_to_log_file(message)
        print(f"\033[1;34m INFO {dt.now()} {message}")
        return True

    def debug(self, message: str):
        # TODO: add doc and implement function
        self._write_to_log_file(message)
        print(message)
        return True

    def warning(self, message: str):
        # TODO: add doc and implement function
        self._write_to_log_file(message)
        print(message)
        return True

    def error(self, message: str):
        # TODO: add doc and implement function
        self._write_to_log_file(message)
        print(message)
        return True

    def _write_to_log_file(self, text: str):
        """
        Writing Log message to log file
        # TODO: needs implementation
        @param text: The text to be logged
        @type text: str
        @return: True
        @rtype: Boolean
        """
        if self.writeToFile:
            # TODO implement writing to file
            return True
        else:
            return True
