"""
Handler File for the AdminTypes
"""

from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import AdminType


class AdminTypeHandler(BaseHandler):
    """
    Handler for the AdminType
    """

    def __init__(self):
        """
        Constructor for the UserHandlerClass
        """
        super().__init__()
        self.dbClass = AdminType
