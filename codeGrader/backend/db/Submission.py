"""
Submission File
This defines the submission class of a task.
"""
from .Base import Base
from .File import File
from .User import User
from .Task import Task
from .Exercise import Exercise
from sqlalchemy import String, Column, DateTime, Integer, func, \
    ForeignKey
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship, backref


class Submission(Base):
    """
    Submission Class
    Ab submission stores the file that was submitted to a Task by a User.
    """
    __tablename__ = 'submission'

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

    # Foreign Keys
    file_id = Column(
        Integer,
        ForeignKey(File.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey(User.id, onupdate="CASCADE"),
        nullable=False,
        index=True
    )

    task_id = Column(
        Integer,
        ForeignKey(Task.id, onupdate="CASCADE"),
        nullable=False
    )

    # Relationships
    file = relationship(
        "File",
        collection_class=ordering_list("id"),
        order_by="[File.id]",
        # cascade is on, so the file will get deleted
        cascade="all",
        passive_deletes=True,
        lazy="subquery"
    )

    user = relationship(
        "User",
        collection_class=ordering_list("id"),
        order_by="[User.id]",
        # cascade="all",
        passive_deletes=True,
        lazy="subquery"
    )

    executionresult = relationship(
        "ExecutionResult",
        collection_class=ordering_list("id"),
        order_by="[ExecutionResult.id]",
        # cascade is on, so the result will get deleted
        cascade="all",
        passive_deletes=True,
        lazy="subquery"
    )

    evaluationresult = relationship(
        "EvaluationResult",
        collection_class=ordering_list("id"),
        order_by="[EvaluationResult.id]",
        # cascade is on, so the result will get deleted
        cascade="all",
        passive_deletes=True,
        lazy="subquery"
    )

    def toJson(self, recursive: bool = True) -> dict:
        """
        JSON representation of a Submission.
        @param recursive: Parameter to indicate if the related items should be loaded and added or not. Default is True
        @type recursive: bool
        @return: The json representation of the Submission
        @rtype: dict
        """

        out = dict()
        out["id"] = self.id
        out["task"] = self.TaskSubmission.toJson()
        out["user"] = self.user.toJson()
        return out
