"""
RPC Server for the evaluation Service.
This RPC Server will be the providing interface for the communication between the backend classes.
@author: mkaiser
"""

from rpyc import Service, exposed, service
from rpyc.utils.server import ThreadedServer
from codeGrader.backend.config import config
from .Evaluation import Evaluation


@service
class EvaluationRPC(Service):
    """
    RPC Server for the evaluation Service
    mkaiser 2023-10-12: just a POC at this point in time.
    """
    server: ThreadedServer

    def __init__(self):
        """
        Constructor for the RPC Server
        :return: No Return
        """
        #self.server = ThreadedServer(EvaluationRPC, port=8002)

    def start(self):
        self.server = ThreadedServer(EvaluationRPC, port=config.evaluationPort)
        self.server.start()

    @exposed
    def hello(self):  # TODO: delete and create proper mapping.
        print("Hello World")

    @exposed
    def evaluate(self, submission_id: int):
        """
        Method to start an evaluation.
        This method will be used in the execution service to signal to the EvaluationService that there is something to evaluate.
        @param submission_id: The id of the ExecutionResult
        @type submission_id: int
        @return:
        """
        raise NotImplementedError
        # start the evaluation for the given submission.


if __name__ == '__main__':
    EvaluationRPC().start()
