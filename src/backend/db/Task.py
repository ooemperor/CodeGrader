"""
Database Model File for a Task with its given column properties.
@author: mkaiser
"""
from src.backend.db.Base import Base
from sqlalchemy import String, Integer, Column, Boolean, Float, Enum, DateTime, Interval, BIGINT, VARCHAR, func, \
    ForeignKey
from src.backend.db.Exercise import Exercise


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
