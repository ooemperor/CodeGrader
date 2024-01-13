
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

    def max_score(self) -> float:
        """
        Calculates the maximal score for this submission, checking all avaible evaluationresults
        @return: The best score for this submission
        @rtype: float
        """
        if len(self.evaluationresult) == 0:
            # there are no evaluation result in the database right now
            return 0.0

        else:
            # there is at least one evaluation in the database
            max_score = 0
            # for loop is needed because we cannot guarantee, that there is only one evaluation in the database
            for result in self.evaluationresult:
                # updating the max score if it is bigger than the current one
                if result.evaluation_score > max_score:
                    max_score = result.evaluation_score

                else:
                    continue
            return max_score*100.0

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
        out["task_id"] = out["task"]["id"]
        out["exercise_id"] = self.TaskSubmission.exercise_id
        out["user"] = self.user.toJson()
        out["user_id"] = out["user"]["id"]
        out["file"] = self.file.toJson(include_binary=False)
        out["file_id"] = self.file.id

        out["evaluations_count"] = len(self.evaluationresult)

        out["max_score"] = self.max_score()

        return out
