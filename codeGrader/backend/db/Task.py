"""
Database Model File for a Task with its given column properties.
@author: mkaiser
"""

from .Base import Base
from .Exercise import Exercise
from sqlalchemy import String, Column, DateTime, BIGINT, func, \
    ForeignKey
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship, backref


class Task(Base):
    """
    Class to represent a Task in the database
    @see: db.Base
    """
    __tablename__ = 'task'

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
    # name of the task that is visible to users
    name = Column(
        String, nullable=False, index=True
    )
    # tag for filtering
    tag = Column(
        String, nullable=True
    )

    # Foreign Keys
    exercise_id = Column(
        BIGINT,
        ForeignKey(Exercise.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    # Relationships

    instructions = relationship(
        "Instruction",
        collection_class=ordering_list("id"),
        order_by="[Instruction.id]",
        cascade="all",
        passive_deletes=True,
        lazy="joined",
        backref=backref("TaskInstruction", lazy="joined")
    )

    attachments = relationship(
        "Attachment",
        collection_class=ordering_list("id"),
        order_by="[Attachment.id]",
        cascade="all",
        passive_deletes=True,
        lazy="joined",
        backref=backref("TaskAttachment", lazy="joined")
    )

    def toJson(self):
        """
        Render the json representation of a Task
        @return: JSON representation of a Task
        @rtype: dict
        """
        out = dict()
        out["id"] = self.id
        out["name"] = self.name
        out["tag"] = self.tag

        if len(self.instructions) == 0:
            out["instructions"] = None
        else:
            _instructions = []
            for instr in self.instructions:
                _instructions.append(instr.toJson())
            out["instructions"] = _instructions

        if len(self.attachments) == 0:
            out["attachments"] = None
        else:
            _attachments = []
            for att in self.attachments:
                _attachments.append(att.toJson())
            out["attachments"] = _attachments

        return out
