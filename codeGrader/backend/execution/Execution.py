"""
This file will later hold the Class of a execution.
This class will define what the execution is and what is to do to get a result.
@author: mkaiser
"""

import os
from codeGrader.backend.config import config
from . import LXC
from codeGrader.backend.db import Session, Submission


class Execution:
    """
    The Execution class that implements e Execution with all its parameters.
    """

    def __init__(self, id_: int):
        """
        Construcotr for a Execution of the code
        @param id_: The id_ of the Submission that was made by a user.
        @type id_: int
        @return: No return for the constructor
        @rtype: None
        """
        self.submissionId = id_
        self.sql_session = Session()
        self.submission = self.sql_session.get_object(Submission, self.submissionId)
        self.lxc = LXC("container_name")

        # parameters that we will set after the execution.
        self.output = None  # the output of the execution.
        self.duration = 0.0  # the duration of the execution
        self.memory_usage = None  # how much memory has approximately been used for running the script

    def execute(self):
        """
        Start the execution of the provided code in the Sandbox and get the output of the evaluation.
        @return: No Return type at the moment
        @todo: implement this function
        """
        raise NotImplementedError # TODO: remove after finishing of the lxc controller
        start_time = time.time()
        self.output = self.lxc.lxc_execute_command("exe")
        end_time = time.time()
        self.duration = end_time - start_time
