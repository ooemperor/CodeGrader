"""
Database Model File for a Subject. Subject can also be used as a Lecture or Topic within a academic understanding.
@author: mkaiser
"""
from src.backend.db.Base import Base
from sqlalchemy import String, Integer, Column, Boolean, Float, Enum, DateTime, Interval, BIGINT, VARCHAR, func, \
    ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list
from src.backend.db.Profile import Profile


class Subject(Base):
    """
    Object to represent a subject
    One Subject holds multiple Exercises
    """
    __tablename__ = 'subject'
    # primary_key
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

    # Foreign key to the Profile Table
    profile_id = Column(
        BIGINT,
        ForeignKey(Profile.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    # Relationships
    exercises = relationship(
        "Exercise",
        collection_class=ordering_list("name"),
        order_by="[Exercise.name]",
        cascade="all",
        passive_deletes=True,
        backref="ExerciseSubject"
    )

    memberships = relationship(
        "Membership",
        collection_class=ordering_list("id"),
        order_by="[Membership.id]",
        cascade="all",
        passive_deletes=True,
        backref="MembershipSubject"
    )

