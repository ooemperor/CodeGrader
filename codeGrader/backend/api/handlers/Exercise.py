"""
Holds the Handlers for everything that corresponds with the Exercise
@author: mkaiser
"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import Exercise


class ExerciseHandler(BaseHandler):
    """
    Handler for the Exercise.
    Using the default get, post, delete and put methods defined in the BaseHandler
    @see: BaseHandler
    """
    def __init__(self) -> None:
        """
        Constructor for the ExerciseHandler
        """
        super().__init__()
        self.dbClass = Exercise
