"""
This file will later hold the RPC Service for the Execution Service.
@author: mkaiser
"""
from rpyc import Service, exposed, service
from rpyc.utils.server import ThreadedServer
from codeGrader.backend.config import config
from codeGrader.backend.execution.Execution import Execution
import rpyc
import threading
import time
import socket


@service
class ExecutionRPC(Service):
    """
    RPC Server for the evaluation Service
    """
    server: ThreadedServer

    def __init__(self):
        """
        empty constructor or the RPC Server
        @return: Nothing
        @rtype: None
        """
        # TODO: Enable this step in the final deployment
        self.evaluationRPC = rpyc.connect(config.evaluationHost, config.evaluationPort).root

    def _authenticator(self, sock: socket.socket):
        ip, port = sock.getpeername()  # reading the source ip and port out of the socket
        if ip in config.executionIpWhiteList:
            self._logging(ip, "Connection Accepted")
            return sock, None
        else:
            self._logging(ip, "Connection refused")
            raise Exception("IP is not in the whitelist. You are not allowed to connect to this rpyc server")

    @staticmethod
    def _logging(ip: str, message: str) -> None:
        """
        Prints a logging message for the ExecutionRPC
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
        """
        Starting the RPC Server
        @return:
        """
        self.server = ThreadedServer(ExecutionRPC, port=config.executionPort, authenticator=self._authenticator)
        self.server.start()

    @exposed
    def addExecution(self, submission_id_ : int) -> bool:
        """
        Adding a execution to the Service for execution.
        @param submission_id_: The id of a submission that has been made
        @type submission_id_: int
        @return: True if successful
        @rtype: Boolean
        """
        threading.Thread(target=self._execution, args=(submission_id_,)).start()
        return True

    def _execution(self, submission_id_: int):
        Execution(submission_id_).execute()
        # start the evaluation by signaling to the evaluationService, that a Execution has finished.
        self.evaluationRPC.evaluate(submission_id_)


if __name__ == '__main__':
    ExecutionRPC().start()
