# CodeGrader - https://github.com/ooemperor/CodeGrader
# Copyright © 2023, 2024 Michael Kaiser <michael.kaiser@emplabs.ch>
#
# This file is part of CodeGrader.
#
# CodeGrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CodeGrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CodeGrader.  If not, see <http://www.gnu.org/licenses/>.

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
        ForeignKey(Profile.id, onupdate="CASCADE"),
        nullable=True,
        index=True
    )

    # Relationships
    exercises = relationship(
        "Exercise",
        collection_class=ordering_list("name"),
        order_by="[Exercise.name]",
        # cascade="all",
        passive_deletes=True,
        lazy="subquery",
        backref=backref("ExerciseSubject", lazy="joined")
    )

    memberships = relationship(
        "Membership",
        collection_class=ordering_list("id"),
        order_by="[Membership.id]",
        # cascade needs to be acitve so when a Subject is deleted the membership is too
        cascade="all",
        passive_deletes=True,
        lazy="noload",
        backref=backref("MembershipSubject", lazy="joined", join_depth=3)
    )

    def get_profile(self) -> dict:
        """
        Get the profile in json representation of the subject
        @return: The Profile in dict form
        """
        if self.SubjectProfile is None:
            return None
        else:
            return self.SubjectProfile.toJson()

    def user_score(self, user_id: int) -> float:
        """
        Processing and Calculation of the Score of a given user for the exercise
        @param user_id: The id of the user to query for.
        @type user_id: int
        @return: The average score of the user for the given exercise
        @rtype: float
        """
        assert user_id is not None
        assert int(user_id) > 0
        score = 0.0
        tasks_count = 0
        for exercise in self.exercises:
            # iterating over all the exercises of the subject.
            for task in exercise.tasks:
                tasks_count += 1
                score += task.user_score(user_id)

        if tasks_count == 0:
            return 0.0
        else:
            average_score = score / tasks_count
            return average_score

    def toJson(self, recursive: bool = True) -> dict:
        """
        Render the json representation of a Subject
        @param recursive: Parameter to indicate if the related items should be loaded and added or not. Default is True
        @type recursive: bool
        @return: JSON representation of a Subject
        @rtype: dict
        """
        out = dict()
        out["id"] = self.id
        out["name"] = self.name
        out["tag"] = self.tag
        # adding profile to json
        out["profile"] = self.get_profile()

        if recursive:
            # adding exercises with tasks to Profile.
            if self.exercises is None:
                out["exercises"] = None
            else:
                _exercises = []
                for exercise in self.exercises:
                    _exercises.append(exercise.toJson())
                out["exercises"] = _exercises
        return out
