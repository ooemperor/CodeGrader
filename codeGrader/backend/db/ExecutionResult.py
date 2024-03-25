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
Database Model File for a ExecutionResult.
@author: mkaiser
"""
from .Base import Base
from .Submission import Submission
from .TestCase import TestCase
from sqlalchemy import Column, DateTime, Integer, func, \
    ForeignKey, UniqueConstraint, String, Double


class ExecutionResult(Base):
    """
    Class to represent a membership of a user to a given Subject.
    Membership is link table between User and Subject.
    """
    __tablename__ = 'executionresult'

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

    execution_output = Column(
        String,
        nullable=False,
        index=False
    )

    execution_exit_code = Column(
        Integer,
        nullable=False,
        index=True
    )

    execution_duration = Column(
        Double,
        nullable=False,
        index=True
    )

    # Foreign Keys
    submission_id = Column(
        Integer,
        ForeignKey(Submission.id, onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    testcase_id = Column(
        Integer,
        ForeignKey(TestCase.id, ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
        index=True
    )

    def toJson(self, recursive: bool = True) -> dict:
        """
        Render the json representation of a ExecutionResult
        @param recursive: Parameter to indicate if the related items should be loaded and added or not. Default is True
        @type recursive: bool
        @return: JSON representation of a Task
        @rtype: dict
        """
        out = dict()
        out["id"] = self.id
        out["output"] = self.execution_output
        out["exit_code"] = self.execution_exit_code
        out["duration"] = self.execution_duration

        out["submission_id"] = self.submission_id
        out["testcase_id"] = self.testcase_id

        return out
