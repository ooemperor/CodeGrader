"""
RPC Server for the evaluation Service.
This RPC Server will be the providing interface for the communication between the backend classes.
@author: mkaiser
"""

from rpyc import Service, exposed, service
from rpyc.utils.server import ThreadedServer


@service
class EvaluationRPC(Service):
    """
    RPC Server for the evaluation Service
    mkaiser 2023-10-12: just a POC at this point in time.
    """

    def __init__(self):
        """
        Constructor for the RPC Server
        :return: No Return
        """
        #self.server = ThreadedServer(EvaluationRPC, port=8002)

    def start(self):
        self.server = ThreadedServer(EvaluationRPC, port=8002)
        self.server.start()

    @exposed
    def hello(self):  # TODO: delete and create proper mapping.
        print("Hello World")

EvaluationRPC().start()