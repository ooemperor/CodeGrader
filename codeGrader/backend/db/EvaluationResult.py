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

    def toJson(self, recursive: bool = True) -> dict:
        """
        Render the json representation of a EvaluationResult
        @param recursive: Parameter to indicate if the related items should be loaded and added or not. Default is True
        @type recursive: bool
        @return: JSON representation of a Task
        @rtype: dict
        """
        out = dict()
        out["id"] = self.id
        out["evaluation_score"] = self.evaluation_score
        out["submission_id"] = self.submission_id

        return out
