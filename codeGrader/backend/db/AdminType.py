"""
File to store the type of an admin
@author: mkaiser
"""

from .Base import Base
from .Profile import Profile
from sqlalchemy import String, Column, DateTime, BIGINT, func, \
    ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.orderinglist import ordering_list


class AdminType(Base):
    """
    Class to store the AdminType
    AdminType describes which type of admin we do have.
    @see: db.Base
    """
    __tablename__ = "admin_type"
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

    def toJson(self) -> dict:
        """
        Render the representation of the AdminType
        @return: JSON representation of a user
        @rtype: String
        """
        out = dict()
        out["id"] = self.id
        out["name"] = self.name
        out["descritption"] = self.description

        return out
