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

    def toJson(self):
        """
        Render the json representation of a admin user
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

        out["admin_type"] = self.type.toJson()

        if self.AdminUserProfile is None:
            out["profile"] = None
        else:
            out["profile"] = self.AdminUserProfile.toJson()

        return out
