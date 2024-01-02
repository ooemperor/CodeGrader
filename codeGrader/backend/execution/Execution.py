"""
This file will later hold the Class of a execution.
This class will define what the execution is and what is to do to get a result.
@author: mkaiser
"""

import os
from codeGrader.backend.config import config
import time
from codeGrader.backend.execution.LXC import LXC
from codeGrader.backend.db import Session, Submission, File, ExecutionResult, Task, Submission
import hashlib


class Execution:
    """
    The Execution class that implements e Execution with all its parameters.
    """

    def __init__(self, id_: int) -> None:
        """
        Construcotr for a Execution of the code
        @param id_: The id_ of the Submission that was made by a user.
        @type id_: int
        @return: No return for the constructor
        @rtype: None
        """
        self.submission_id = id_
        self.submission = Session().get_object(Submission, self.submission_id)
        self.scriptFile = self.submission.file  # the file
        self.task = self.submission.TaskSubmission  # the task object for the submission
        self.testcases = self.task.testcases  # list of all the testcases for the task of the submission

        # creating a hash value to extend the lxc name with for unique name
        self.lxc_name = f"{self.submission.user.username}_{self.task.id}_{self.submission_id}"
        self.lxc = LXC(self.lxc_name)

        # parameters that we will set after the execution.
        self.output = None  # the output of the execution.
        self.returncode = None  # the returncode of the execution
        self.duration = 0.0  # the duration of the execution
        self.memory_usage = None  # how much memory has approximately been used for running the script

    def _prepare(self) -> None:
        """
        Prepare the lxc container for the execution
        This includes installing the compilers/interpreters
        @return: Nothing
        @rtype: None
        """
        while self.lxc.ip is None:
            self.lxc.lxc_get_info()
        self.lxc.lxc_execute_command("apt install python3 -y")  # TODO dont make this hardcoded

    def cleanup(self) -> None:
        """
        Cleanup after the execution
        @return: Nothing
        @rtype: None
        """
        self.lxc.lxc_stop()
        self.lxc.lxc_destroy()

    def execute(self) -> None:
        """
        Start the execution of the provided code in the Sandbox and get the output of the evaluation.
        @return: No Return type at the moment
        @todo: we need to run all the testcases that we find for the given Submission-Task
        """
        self.lxc.lxc_start()
        self._prepare()

        # uploading the submission file
        script_filename_hash = str(hashlib.sha256(self.scriptFile.filename.encode('UTF-8')).hexdigest())
        self.lxc.lxc_upload_file("/opt", script_filename_hash, self.scriptFile.getFileContent())

        if len(self.testcases) > 0:
            # there are testcases avaible
            for testcase in self.testcases:
                file = testcase.input_file
                testcase_file_hash = str(hashlib.sha256(file.filename.encode('UTF-8')).hexdigest())
                self.lxc.lxc_upload_file("/opt", testcase_file_hash,
                                         file.getFileContent())  # uploading the individual task file

                start_time = time.time()

                output, returncode = self.lxc.lxc_execute_command(
                    f"python3 {config.executionFilePath}/{script_filename_hash} < {testcase_file_hash}")  # TODO make better execution function. Not allowed to be hardcoded

                end_time = time.time()

                duration = end_time - start_time
                self.duration = duration

                self._addExecutionResult(output, returncode, duration, testcase.id)

        elif len(self.testcases) == 0:
            # no testcases have been found. we just execute it without testcases

            start_time = time.time()
            output, returncode = self.lxc.lxc_execute_command(
                f"python3 {config.executionFilePath}/{script_filename_hash}")  # TODO make better execution function. Not allowed to be hardcoded
            end_time = time.time()
            duration = end_time - start_time
            self._addExecutionResult()
            self._addExecutionResult(output, returncode, duration)

        # since the execution is done we clean up after and destroy the lxc, create the Result entries in the database
        self.cleanup()

    def _addExecutionResult(self, output: str, returncode: str, duration: float, testcase_id: int = None) -> None:
        """
        Creating a ExecutionResultentry in the database with values provided by the function parameters
        @param output: the output of a single execution
        @type output: str
        @param returncode: the return code of the execution
        @type returncode: str
        @param duration: the duration of the execution
        @type duration: float
        @param testcase_id: The id of the testcase of the individual execution
        @type testcase_id: int
        @return: Nothing
        @rtype: None
        """

        data = dict()
        data["execution_output"] = output
        data["execution_exit_code"] = returncode
        data["execution_duration"] = duration
        data["submission_id"] = self.submission_id
        data["testcase_id"] = testcase_id

        exec_result = ExecutionResult(**data)

        Session().create(exec_result)

    def _addExecutionResult(self) -> None:
        """
        Creating a ExecutionResultentry in the database.
        @return: Nothing
        @rtype: None
        """

        data = dict()
        data["execution_output"] = self.output
        data["execution_exit_code"] = self.returncode
        data["execution_duration"] = self.duration
        data["submission_id"] = self.submission_id

        exec_result = ExecutionResult(**data)

        Session().create(exec_result)
