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
File to store the type of an evaluation
@author: mkaiser
"""

from .Base import Base
from .Profile import Profile
from sqlalchemy import String, Column, DateTime, BIGINT, func, \
    ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.orderinglist import ordering_list


class EvaluationType(Base):
    """
    Class to store the EvaluationType
    EvaluationType describes which type of evaluation a task has/is
    @see: db.Base
    """
    __tablename__ = "evaluation_type"
    # primary key
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
    # the name for the type
    name = Column(
        String, nullable=False, unique=True, index=True
    )
    description = Column(
        String, nullable=True, unique=False
    )

    def toJson(self, recursive: bool = True) -> dict:
        """
        Render the representation of the EvaluationType
        @param recursive: Parameter to indicate if the related items should be loaded and added or not. Default is True
        @type recursive: bool
        @return: JSON representation of a user
        @rtype: String
        """
        out = dict()
        out["id"] = self.id
        out["name"] = self.name
        out["descritption"] = self.description

        return out
