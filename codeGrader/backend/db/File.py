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
Database Model to store a File (Attachment or Submission and more).
@author: mkaiser
"""
import io

from .Base import Base
from sqlalchemy import String, Integer, Column, Boolean, DateTime, func, \
    LargeBinary
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.orderinglist import ordering_list


class File(Base):
    """
    Class to store a file in the database
    """
    __tablename__ = "file"
    # primary key
    id = Column(
        Integer, primary_key=True, index=True
    )
    # Datetimestamp of creation in the database
    creation_dts = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    # Datetimestamp of the last update in the database
    updated_dts = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    filename = Column(
        String, nullable=False, index=True
    )
    # the file type. e.g .pdf, .py and more
    fileExtension = Column(
        String, nullable=False
    )
    #  the file directly in the database, not beautiful but worth a test
    file = Column(
        LargeBinary, nullable=False
    )

    instruction = relationship(
        "Instruction",
        collection_class=ordering_list("id"),
        order_by="[Instruction.id]",
        cascade="all",
        passive_deletes=True,
        lazy="noload",
        backref=backref("InstructionFile", lazy="joined", cascade="all, delete")
    )

    attachments = relationship(
        "Attachment",
        collection_class=ordering_list("id"),
        order_by="[Attachment.id]",
        cascade="all, delete",
        passive_deletes=True,
        lazy="noload",
        backref=backref("AttachmentFile", lazy="joined", cascade="all, delete")
    )

    def getFileContent(self) -> memoryview:
        """
        Getting the content of a file a returning it
        @return: Content of file
        @rtype: memoryview
        """
        return io.BytesIO(self.file).getbuffer()

    def toJson(self, include_binary: bool = True, recursive: bool = True) -> dict:
        """
        Render the json representation of a File
        @param include_binary: if the Binary Data of the file should also be provided or not.
        @type include_binary: Boolean
        @param recursive: Parameter to indicate if the related items should be loaded and added or not. Default is True
        @type recursive: bool
        @return: JSON representation of a profile
        @rtype: dict
        """
        out = dict()
        out["id"] = self.id
        out["filename"] = self.filename
        out["fileExtension"] = self.fileExtension
        if include_binary:
            out["file"] = self.file
        return out
