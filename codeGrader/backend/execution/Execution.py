"""
This file will later hold the Class of a execution.
This class will define what the execution is and what is to do to get a result.
@author: mkaiser
"""

import os
from codeGrader.backend.config import config
import time
from .LXC import LXC
from codeGrader.backend.db import Session, Submission, File, ExecutionResult


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
        self.submission = Session().get_object(Submission, self.submissionId)
        self.scriptFile = self.submission.file
        self.lxc = LXC("container_name")


        # parameters that we will set after the execution.
        self.output = None  # the output of the execution.
        self.returncode = None  # the returncode of the execution
        self.duration = 0.0  # the duration of the execution
        self.memory_usage = None  # how much memory has approximately been used for running the script

    def _prepare(self):
        """
        Prepare the lxc container for the execution
        This includes installing the compilers/interpreters
        @return: Nothing
        @rtype: None
        """
        while self.lxc.ip is None:
            self.lxc.lxc_get_info()
        self.lxc.lxc_execute_command("apt install python3 -y")  # TODO dont make this hardcoded

    def cleanup(self):
        """
        Cleanup after the execution
        @return: Nothing
        @rtype: None
        """
        self.lxc.lxc_stop()
        self.lxc.lxc_destroy()

    def execute(self):
        """
        Start the execution of the provided code in the Sandbox and get the output of the evaluation.
        @return: No Return type at the moment
        @todo: implement this function
        """
        self.lxc.lxc_start()
        self._prepare()

        self.lxc.lxc_upload_file("/opt", self.scriptFile.filename, self.scriptFile.getFileContent())
        start_time = time.time()
        self.output, self.returncode = self.lxc.lxc_execute_command(
            f"python3 {config.executionFilePath}/{self.scriptFile.filename}")  # TODO make better execution function.
        end_time = time.time()
        self.duration = end_time - start_time

        # since the execution is done we cleanup after and destroy the lxc, create the Result entries in the database
        self.cleanup()
        self._addExecutionResult()

    def _addExecutionResult(self):
        """
        Creating a ExecutionResultentry in the database.
        @return: Nothing
        @rtype: None
        """

        data = dict()
        data["execution_output"] = self.output
        data["execution_exit_code"] = self.returncode
        data["execution_duration"] = self.duration
        data["submission_id"] = self.submissionId

        exec_result = ExecutionResult(**data)

        Session().create(exec_result)
