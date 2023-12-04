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
        out_["instruction_id"] = self.id
        out_["file"] = self.InstructionFile.toJSON(include_binary=False)
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

    def toJson(self) -> dict:
        """
        Render the json representation of a Attachment
        This is a relation table, so we get just the values of the related tables.
        @return: JSON representation of a profile
        @rtype: dict
        """
        out_ = dict()
        out_["instruction_id"] = self.id
        out_["file"] = self.AttachmentFile.toJSON(include_binary=False)
        return out_

