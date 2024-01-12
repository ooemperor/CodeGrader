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
Database Model File for a AdminUser with its given column properties.
@author: mkaiser
"""

from .Base import Base
from .Profile import Profile
from .AdminType import AdminType
from sqlalchemy import String, Column, DateTime, BIGINT, func, \
    ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.orderinglist import ordering_list


class AdminUser(Base):
    """
    Class to store all the administrator users
    """
    __tablename__ = 'adminuser'
    # primary key
    id = Column(
        Integer, primary_key=True, index=True
    )
    creation_dts = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    # Datetimestamp of the last update in the database
    updated_dts = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    username = Column(
        String, nullable=False, unique=True, index=True
    )
    first_name = Column(
        String, nullable=False
    )
    last_name = Column(
        String, nullable=False
    )
    email = Column(
        String, nullable=False
    )
    password = Column(
        String, nullable=False  # password will be stored in hash form in database
    )
    # usertag for filtering
    tag = Column(
        String, nullable=True
    )

    # Foreign Key to the Admin Type Table
    admin_type = Column(
        Integer,
        ForeignKey(AdminType.id),
        nullable=False,
        index=True
    )


    # Foreign key to the Profile Table
    profile_id = Column(
        Integer,
        ForeignKey(Profile.id),
        nullable=True,
        index=True
    )

    type = relationship(
        "AdminType",
        collection_class=ordering_list("id"),
        order_by="[AdminType.id]",
        passive_deletes=True,
        lazy="joined"
    )

    def toJson(self, recursive: bool = True) -> dict:
        """
        Render the json representation of a admin user
        @param recursive: Parameter to indicate if the related items should be loaded and added or not. Default is True
        @type recursive: bool
        @return: JSON representation of a admin user
        @rtype: String
        """
        out = dict()
        out["id"] = self.id
        out["username"] = self.username
        out["first_name"] = self.first_name
        out["last_name"] = self.last_name
        out["email"] = self.email
        out["tag"] = self.tag

        if recursive:
            out["admin_type"] = self.type.toJson(recursive=True)

            if self.AdminUserProfile is None:
                out["profile"] = None
            else:
                out["profile"] = self.AdminUserProfile.toJson()

        return out
