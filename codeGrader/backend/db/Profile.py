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
Database Model File for storing all the profiles that we are using. This introduces the capability to later on filter by profile
@author: mkaiser
"""
from .Base import Base
from sqlalchemy import String, Integer, Column, DateTime, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.orderinglist import ordering_list


class Profile(Base):
    """
    Class to represent a profile. The profile makes the application multi-client capable.
    """
    __tablename__ = "profile"
    # primary key
    id = Column(
        Integer, primary_key=True, index=True
    )
    # Datetimestamp of creation in the database
    creation_dts = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    # Datetimestamp of the last update in the database
    updated_dts = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    # name of the profile
    name = Column(
        String, nullable=False, unique=True, index=True
    )
    # tag for filtering
    tag = Column(
        String, nullable=True
    )

    # relationships
    # relationship to which users have this profile
    users = relationship(
        "User",
        collection_class=ordering_list("username"),
        order_by="[User.username]",
        # cascade="all",
        passive_deletes=True,
        lazy="joined",
        backref=backref("UserProfile", lazy="joined")
    )

    # relationship to the adminusers
    adminUsers = relationship(
        "AdminUser",
        collection_class=ordering_list("username"),
        order_by="[AdminUser.username]",
        # cascade="all",
        passive_deletes=True,
        lazy="joined",
        backref=backref("AdminUserProfile", lazy="joined")
    )

    #relationships to the subjects
    subjects = relationship(
        "Subject",
        collection_class=ordering_list("name"),
        order_by="[Subject.name]",
        # cascade="all",
        passive_deletes=True,
        lazy="noload",
        backref=backref("SubjectProfile", lazy="joined")
    )

    def toJson(self, recursive: bool = True) -> dict:
        """
        Render the json representation of a Profile
        @param recursive: Parameter to indicate if the related items should be loaded and added or not. Default is True
        @type recursive: bool
        @return: JSON representation of a profile
        @rtype: dict
        """
        out = dict()
        out["id"] = self.id
        out["name"] = self.name
        out["tag"] = self.tag
        return out

