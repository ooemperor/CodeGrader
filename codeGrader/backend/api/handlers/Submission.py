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
        t1 = threading.Thread(target=execution_rpyc.addExecution, args=(submission_id_,))
        t1.start()
        return True