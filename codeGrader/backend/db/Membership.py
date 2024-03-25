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
Database Model File for a Membership.
@author: mkaiser
"""
from .Base import Base
from .User import User
from .Subject import Subject
from sqlalchemy import Column, DateTime, Integer, func, \
    ForeignKey, UniqueConstraint


class Membership(Base):
    """
    Class to represent a membership of a user to a given Subject.
    Membership is link table between User and Subject.
    """
    __tablename__ = 'membership'
    __table_args__ = (UniqueConstraint("user_id", "subject_id"),)  # last comma necessary to avoid error message of data type

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

    # Foreign Keys:
    user_id = Column(
        Integer,
        ForeignKey(User.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    subject_id = Column(
        Integer,
        ForeignKey(Subject.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    def toJson(self, recursive: bool = True) -> dict:
        """
        Render the representation of a Membership.
        Membership is link between user and subject.
        @param recursive: Parameter to configure if the values of the related objects shall also be loaded. Default is True
        @type recursive: bool
        @return: The json Representation of the Membership
        @rtype: dict
        """
        out = dict()
        out["id"] = self.id
        out["user_id"] = self.user_id
        out["subject_id"] = self.subject_id

        if recursive:
            out["user"] = self.MembershipUser.toJson(recursive=False)
            out["subject"] = self.MembershipSubject.toJson(recursive=False)

        return out
