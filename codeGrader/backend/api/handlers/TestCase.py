"""
Holds the Handlers for everything that corresponds with the TestCases
@author: mkaiser
"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import TestCase


class TestCaseHandler(BaseHandler):
    """
    Handler for the TestCase Class.
    Using the default get, post, delete and put methods defined in the
    @see: BaseHandler
    """
    def __init__(self):
        """
        Constructor for the ProfileHandler
        """
        super().__init__()
        self.dbClass = TestCase
