"""
Class to implement a Worker for running tasks out of queues.
@author: mkaiser
"""

from codeGrader.backend.config import config
from multiprocessing import Process, Queue
from time import sleep


class Worker(Process):
    """
    Class for a worker that can execute a given task. Each worker populates one Process of the host system
    """
    def __init__(self, process_queue: Queue):
        self.queue = process_queue
        self.occupied = False

    def run(self):
        """
        Run function for the worker.
        @return:
        """
        while True:
            if self.queue.empty():
                # wait 5 seconds until we have another job.
                sleep(5)
            else:
                job = self.queue.get()
                self.occupied = True
                job.start()
                self.occupied = False

    def isOccupied(self):
        """
        Get the occupation State of the Worker.
        @return: True or false depending if the worker is occupied or not.
        @rtype: bool
        """
        return self.occupied

