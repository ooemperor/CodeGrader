"""
This file will later hold the RPC Service for the Execution Service.
@author: mkaiser
"""

from rpyc import Service, exposed, service
from rpyc.utils.server import ThreadedServer
from codeGrader.backend.config import config
from .Execution import Execution
import rpyc


@service
class EvaluationRPC(Service):
    """
    RPC Server for the evaluation Service
    mkaiser 2023-10-12: just a POC at this point in time.
    """
    server: ThreadedServer

    def __init__(self):
        """
        empty constructor or the RPC Server
        @return: Nothing
        @rtype: None
        """
        self.evaluationRPC = rpyc.connect(config.evaluationHost, config.evaluationPort).root

    def start(self):
        """
        Starting the RPC Server
        @return:
        """
        self.server = ThreadedServer(EvaluationRPC, port=config.executionPort)
        self.server.start()

    @exposed
    def addEvaluation(self, submission_id_ : int):
        """
        Adding a execution to the Service for execution.
        @param submission_id_: The id of a submission that has been made
        @type submission_id_: int
        @return: True if successful
        @rtype: Boolean
        """
        Execution(submission_id_).execute()
        # TODO: write the result of the execution in the database for the given submission.

        # start the evaluation by signaling to the evaluationService, that a Execution has finished.
        self.evaluationRPC.evaluate(submission_id_)


if __name__ == '__main__':
    EvaluationRPC().start()