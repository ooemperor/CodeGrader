"""
Database Model File for a Membership.
@author: mkaiser
"""
from .Base import Base
from .User import User
from .Subject import Subject
from sqlalchemy import Column, DateTime, BIGINT, func, \
    ForeignKey, UniqueConstraint


class Membership(Base):
    """
    Class to represent a membership of a user to a given Subject.
    Membership is link table between User and Subject.
    """
    __tablename__ = 'membership'
    __table_args__ = (UniqueConstraint("user_id", "subject_id"),)  # last comma necessary to avoid error message of data type

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

    # Foreign Keys:
    user_id = Column(
        BIGINT,
        ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    subject_id = Column(
        BIGINT,
        ForeignKey(Subject.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
