"""
Holds the Handlers for everything that corresponds with the Exercise
@author: mkaiser
# TODO: Handle Errors while parsing information or querying the database
# TODO: Define and document proper response after put and post operations.

"""
from src.backend.handlers.Base import BaseHandler
from src.backend.db import Exercise


class ExerciseHandler(BaseHandler):
    """
    Handler for the Exercise.
    Using the default get, post, delete and put methods defined in the BaseHandler
    @see: BaseHandler
    """
    def __init__(self):
        """
        Constructor for the ExerciseHandler
        """
        super().__init__()
        self.dbClass = Exercise
