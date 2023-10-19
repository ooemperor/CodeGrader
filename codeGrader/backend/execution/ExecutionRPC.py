"""
This file will later hold the RPC Service for the Execution Service.
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

    def start(self):
        self.server = ThreadedServer(EvaluationRPC, port=8002)
        self.server.start()