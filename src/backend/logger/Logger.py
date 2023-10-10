"""
Defining the logger class for the CodeGrader
Writing the own logger class for better control of the logged messages.

@author: mkaiser
"""

from datetime import datetime as dt
from src.backend.config import config


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

    def info(self, message):
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

    def debug(self, message):
        # TODO: add doc and implement function
        self._write_to_log_file(message)
        print(message)
        return True

    def warning(self, message):
        # TODO: add doc and implement function
        self._write_to_log_file(message)
        print(message)
        return True

    def error(self, message):
        # TODO: add doc and implement function
        self._write_to_log_file(message)
        print(message)
        return True

    def _write_to_log_file(self, text):
        """
        Writing Log message to log file
        # TODO: needs implementation
        @param text: The text to be logged
        @type text: str
        @return: True
        @rtype: Boolean
        """
        if self.writeToFile:
            # implement writing to file
            return True
        else:
            return True
