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
Contains every type of attachment for the Tasks and possible other classes, e.g. Instructions, Code Snippets and more.
Instruction and Attachment are getting partioned horizontally. This makes for easier relationships on the task object.
@author: mkaiser
"""

from .Base import Base
from .Task import Task
from .File import File
from sqlalchemy import Column, DateTime, BIGINT, func, \
    ForeignKey


class Instruction(Base):
    """
    The Instructions for a task. This is a link class, that links the task to a File.
    """

    __tablename__ = 'instruction'

    id = Column(
        BIGINT, primary_key=True, index=True
    )
    # Datetimestamp of creation in the database
    creation_dts = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    # Datetimestamp of the last update in the database
    updated_dts = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ForeignKeys
    task_id = Column(
        BIGINT,
        ForeignKey(Task.id, onupdate="CASCADE"),
        nullable=True,
        index=True
    )

    file_id = Column(
        BIGINT,
        ForeignKey(File.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    def toJson(self) -> dict:
        """
        Render the json representation of a Instruction
        This is a relation table, so we get just the values of the related tables.
        @return: JSON representation of a profile
        @rtype: dict
        """
        out_ = dict()
        out_["id"] = self.id
        out_["file"] = self.InstructionFile.toJson(include_binary=False)
        return out_


class Attachment(Base):
    """
    The Attachment for a task. This is a link class, that links the task to a File.
    """

    __tablename__ = 'attachment'

    id = Column(
        BIGINT, primary_key=True, index=True
    )
    # Datetimestamp of creation in the database
    creation_dts = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    # Datetimestamp of the last update in the database
    updated_dts = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # ForeignKeys
    task_id = Column(
        BIGINT,
        ForeignKey(Task.id, onupdate="CASCADE"),
        nullable=True,
        index=True
    )

    file_id = Column(
        BIGINT,
        ForeignKey(File.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    def toJson(self, recursive: bool = True) -> dict:
        """
        Render the json representation of a Attachment
        This is a relation table, so we get just the values of the related tables.
        @param recursive: Parameter to indicate if the related items should be loaded and added or not. Default is True
        @type recursive: bool
        @return: JSON representation of a profile
        @rtype: dict
        """
        out_ = dict()
        out_["id"] = self.id
        out_["file"] = self.AttachmentFile.toJson(include_binary=False)
        return out_

