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
Holds the Handlers for everything that corresponds with the Submission Class.
@author: mkaiser
"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import Submission
from codeGrader.backend.config import config
import rpyc
import threading


class SubmissionHandler(BaseHandler):
    """
    Handler for the Submission Class.
    Using the default get, post, delete and put methods defined in the BaseHandler
    @see: BaseHandler
    """
    def __init__(self) -> None:
        """
        Constructor for the ProfileHandler
        """
        super().__init__()
        self.dbClass = Submission

    @staticmethod
    def signal_execution_service(submission_id_: int) -> bool:
        """
        Send a signal to the execution service to start the execution
        The execution is made as a thread paralell to the
        @param submission_id_: The id of the submission that has been made
        @type submission_id_: int
        @return: True on success, else will raise an error
        @rtype: bool
        """
        execution_rpyc = rpyc.connect(config.executionHost, config.executionPort).root
        return_value = execution_rpyc.addExecution(submission_id_)
        return True