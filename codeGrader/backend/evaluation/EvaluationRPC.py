"""
RPC Server for the evaluation Service.
This RPC Server will be the providing interface for the communication between the backend classes.
@author: mkaiser
"""

from rpyc import Service, exposed, service
from rpyc.utils.server import ThreadedServer
from codeGrader.backend.config import config
from codeGrader.backend.evaluation.EvaluationController import EvaluationController
import threading
import time
import socket

@service
class EvaluationRPC(Service):
    """
    RPC Server for the evaluation Service
    mkaiser 2023-10-12: just a POC at this point in time.
    """
    server: ThreadedServer

    def __init__(self) -> None:
        """
        Constructor for the RPC Server
        :return: No Return
        """
        #self.server = ThreadedServer(EvaluationRPC, port=8002)

    def _authenticator(self, sock: socket.socket):
        ip, port = sock.getpeername()  # reading the source ip and port out of the socket
        if ip in config.executionIpWhiteList:
            self._logging(ip, "Connection Accepted")
            return sock, None
        else:
            self._logging(ip, "Connection refused")
            raise Exception("IP is not in the whitelist. You are not allowed to connect to this rpyc server")

    @staticmethod
    def _logging(self, ip: str, message: str) -> None:
        """
        Prints a logging message for the EvaluationRPC
        @param ip: The source IP Adress of the Connection
        @type ip: str
        @param message: The message to be logged
        @type message: str
        @return: No Return
        @rtype: None
        """
        current_time = time.strftime("%d/%m/%y %H:%M:%S", time.localtime())
        print(f"{current_time} {ip} {message}")

    def start(self) -> None:
        self.server = ThreadedServer(EvaluationRPC, port=config.evaluationPort, authenticator=self._authenticator)
        self.server.start()

    @exposed
    def evaluate(self, submission_id: int) -> bool:
        """
        Method to start an evaluation.
        This method will be used in the execution service to signal to the EvaluationService that there is something to evaluate.
        @param submission_id: The id of the ExecutionResult
        @type submission_id: int
        @return: True if succesful, else error
        """
        threading.Thread(target=self._evaluate, args=(submission_id,)).start()
        return True

    @staticmethod
    def _evaluate(self, submission_id:int) -> None:
        EvaluationController(submission_id).evaluate()


if __name__ == '__main__':
    EvaluationRPC().start()
