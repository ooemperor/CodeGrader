"""
Database Model File for the EvaluationResult
@author: mkaiser
"""
from .Base import Base
from .Submission import Submission
from .ExecutionResult import ExecutionResult
from sqlalchemy import Column, DateTime, Integer, func, \
    ForeignKey, UniqueConstraint, String, Float


class EvaluationResult(Base):
    """
    Class to store the EvaluationResult for a given
    Membership is link table between User and Subject.
    """
    __tablename__ = 'evaluationresult'

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

    evaluation_score = Column(
        Float,
        nullable=False,
        index=False
    )

    # Foreign Keys
    submission_id = Column(
        Integer,
        ForeignKey(Submission.id, onupdate="CASCADE"),
        nullable=True,
        index=True
    )
