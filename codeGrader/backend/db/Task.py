"""
Database Model File for a Task with its given column properties.
@author: mkaiser
"""

from .Base import Base
from .Exercise import Exercise
from sqlalchemy import String, Column, DateTime, Integer, func, \
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
        Integer, primary_key=True, index=True
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
        Integer,
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
        lazy="subquery",
        backref=backref("TaskInstruction", lazy="subquery")
    )

    attachments = relationship(
        "Attachment",
        collection_class=ordering_list("id"),
        order_by="[Attachment.id]",
        cascade="all",
        passive_deletes=True,
        lazy="subquery",
        backref=backref("TaskAttachment", lazy="subquery")
    )

    submissions = relationship(
        "Submission",
        collection_class=ordering_list("id"),
        order_by="[Submission.id]",
        cascade="all",
        passive_deletes=True,
        lazy="subquery",
        backref=backref("TaskSubmission", lazy="subquery")
    )

    testcases = relationship(
        "TestCase",
        collection_class=ordering_list("id"),
        order_by="[TestCase.id]",
        cascade="all",
        passive_deletes=True,
        lazy="subquery",
        backref=backref("TaskTestCase", lazy="subquery")
    )

    def get_profile(self) -> dict:
        """
        Get the profile via the parent object if avaible
        @return: The Profile in dict form
        @rtype: dict
        """
        if self.TaskExercise is None:
            return None
        else:
            return self.TaskExercise.get_profile()

    def toJson(self, recursive: bool = True) -> dict:
        """
        Render the json representation of a Task
        @param recursive: Parameter to indicate if the related items should be loaded and added or not. Default is True
        @type recursive: bool
        @return: JSON representation of a Task
        @rtype: dict
        """
        out = dict()
        out["id"] = self.id
        out["name"] = self.name
        out["tag"] = self.tag

        if recursive:

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

            out["profile"] = self.get_profile()
        return out
