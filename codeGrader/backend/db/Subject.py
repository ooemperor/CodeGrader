"""
Database Model File for a Subject. Subject can also be used as a Lecture or Topic within a academic understanding.
@author: mkaiser
"""
from .Base import Base
from .Profile import Profile
from sqlalchemy import String, Column, DateTime, Integer, func, \
    ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.orderinglist import ordering_list


class Subject(Base):
    """
    Object to represent a subject
    One Subject holds multiple Exercises
    """
    __tablename__ = 'subject'
    # primary_key
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

    # Foreign key to the Profile Table
    profile_id = Column(
        Integer,
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
        lazy="joined",
        backref=backref("ExerciseSubject", lazy="noload")
    )

    memberships = relationship(
        "Membership",
        collection_class=ordering_list("id"),
        order_by="[Membership.id]",
        cascade="all",
        passive_deletes=True,
        lazy="joined",
        backref=backref("MembershipSubject", lazy="joined")
    )

    def toJson(self):
        """
        Render the json representation of a Subject
        @return: JSON representation of a Subject
        @rtype: dict
        """
        out = dict()
        out["id"] = self.id
        out["name"] = self.name
        out["tag"] = self.tag
        # adding profile to json
        if self.SubjectProfile is None:
            out["profile"] = None
        else:
            out["profile"] = self.SubjectProfile.toJson()

        # adding exercises with tasks to Profile.
        if self.exercises is None:
            out["exercises"] = None
        else:
            _exercises = []
            for exercise in self.exercises:
                _exercises.append(exercise.toJson())
            out["exercises"] = _exercises
        return out

