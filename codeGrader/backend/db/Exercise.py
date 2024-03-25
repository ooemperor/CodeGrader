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
Database Model File for a Exercise.
@author: mkaiser
"""
from .Base import Base
from .Subject import Subject
from sqlalchemy import String, Column, DateTime, Integer, func, \
    ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.orderinglist import ordering_list
from .Session import Session


class Exercise(Base):
    """
    Class that represents a exercise.
    Exercise holds multiple tasks (is a Group of tasks)
    """

    __tablename__ = 'exercise'

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

    description = Column(
        String, nullable=True
    )

    # tag for filtering
    tag = Column(
        String, nullable=True
    )

    # Foreign Keys
    subject_id = Column(
        Integer,
        ForeignKey(Subject.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    tasks = relationship(
        "Task",
        collection_class=ordering_list("name"),
        order_by="[Task.name]",
        # cascade="all",
        passive_deletes=True,
        lazy="subquery",
        join_depth=3,
        backref=backref("TaskExercise", lazy="joined", join_depth=3)
    )

    def get_profile(self):
        if self.ExerciseSubject is None:
            return None
        else:
            return self.ExerciseSubject.get_profile()

    def user_score(self, user_id: int) -> float:
        """
        Processing and Calculation of the Score of a given user for the exercise
        @param user_id: The id of the user to query for.
        @type user_id: int
        @return: The average score of the user for the given exercise
        @rtype: float
        """
        assert user_id is not None
        assert user_id > 0
        score = 0.0
        for task in self.tasks:
            score += task.user_score(user_id)  # reading the score from the task
        if len(self.tasks) == 0:
            return 0.0
        else:
            average_score = score / (len(self.tasks))
            return average_score

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

        if self.description is not None:
            out["description"] = self.description
        else:
            out["description"] = ""

        if recursive:
            if self.tasks is None:
                out["tasks"] = None
            else:
                _tasks = []
                for task in self.tasks:
                    _tasks.append(task.toJson())
                out["tasks"] = _tasks

            out["profile"] = self.get_profile()

            if self.subject_id is None:
                out["subject"] = None
                out["subject_id"] = None
            else:
                out["subject"] = self.ExerciseSubject.toJson(recursive=False)
                out["subject_id"] = self.subject_id

        return out
