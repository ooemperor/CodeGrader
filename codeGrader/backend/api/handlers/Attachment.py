# CodeGrader - https://github.com/ooemperor/CodeGrader
# Copyright © 2023, 2024 Michael Kaiser <michael.kaiser@emplabs.ch>
#
# This file is part of CodeGrader.
#
# CodeGrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CodeGrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CodeGrader.  If not, see <http://www.gnu.org/licenses/>.

"""
Holds the Handlers for everything that corresponds with the Submission Class.
@author: mkaiser
"""
from codeGrader.backend.api.handlers.Base import BaseHandler
from codeGrader.backend.db import Attachment


class AttachmentHandler(BaseHandler):
    """
    Handler for the Attachment Class
    Using the default get, post, delete and put methods defined in the BaseHandler
    @see: BaseHandler
    """
    def __init__(self) -> None:
        """
        Constructor for the AttachmentHandler
        """
        super().__init__()
        self.dbClass = Attachment
