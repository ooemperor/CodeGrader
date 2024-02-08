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

    description = Column(
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

    def user_score(self, user_id: int) -> float:
        """
        Processing and Calculation of the Score of a given user for the task
        @param user_id: The id of the user to query for.
        @type user_id: int
        @return: The score of the user for the given task
        @rtype: float
        """
        assert user_id is not None
        assert int(user_id) > 0
        score = 0.0
        for sub in self.submissions:
            if sub.user.id == user_id:
                temp_score = sub.max_score()

                if temp_score > score:
                    score = temp_score

        return score  # max score has been found, so we return it

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
        if self.TaskExercise is None:
            out["exercise"] = None
            out["subject_id"] = None
        else:
            out["exercise"] = self.TaskExercise.toJson(recursive=False)
            out["subject_id"] = self.TaskExercise.subject_id

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
