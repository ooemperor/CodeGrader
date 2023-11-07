"""
Database Model File for a ExecutionResult.
@author: mkaiser
"""
from .Base import Base
from .Submission import Submission
from .TestCase import TestCase
from sqlalchemy import Column, DateTime, Integer, func, \
    ForeignKey, UniqueConstraint, String, Double


class ExecutionResult(Base):
    """
    Class to represent a membership of a user to a given Subject.
    Membership is link table between User and Subject.
    """
    __tablename__ = 'executionresult'

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

    execution_output = Column(
        String,
        nullable=False,
        index=False
    )

    execution_exit_code = Column(
        Integer,
        nullable=False,
        index=True
    )

    execution_duration = Column(
        Double,
        nullable=False,
        index=True
    )

    # Foreign Keys
    submission_id = Column(
        Integer,
        ForeignKey(Submission.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    testcase_id = Column(
        Integer,
        ForeignKey(TestCase.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
