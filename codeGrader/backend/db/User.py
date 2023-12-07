"""
Database Model File for a user with its given column properties.
@author: mkaiser
"""
from .Base import Base
from .Profile import Profile
from sqlalchemy import String, Column, DateTime, BIGINT, func, \
    ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.orderinglist import ordering_list


class User(Base):
    """
    Class to represent a User in the database
    @see: db.Base
    """

    __tablename__ = "user"
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
    # username for login
    username = Column(
        String, nullable=False, unique=True, index=True
    )
    first_name = Column(
        String, nullable=False
    )
    last_name = Column(
        String, nullable=False
    )
    # email adress for password reset and more
    email = Column(
        String, nullable=False
    )
    # password stored in hash
    password = Column(
        String, nullable=False  # password will be stored in hash form in database
    )
    # usertag for filtering
    tag = Column(
        String, nullable=True
    )
    # Foreign Keys
    # Foreign key to the Profile Table
    profile_id = Column(
        Integer,
        ForeignKey(Profile.id),
        nullable=True,
        index=True
    )

    # Relationships
    memberships = relationship(
        "Membership",
        collection_class=ordering_list("id"),
        order_by="[Membership.id]",
        cascade="all",
        passive_deletes=True,
        lazy="joined",
        backref=backref("MembershipUser", lazy="joined")
    )

    def toJson(self, recursive: bool = True) -> dict:
        """
        Render the json representation of a user
        @param recursive: Parameter to indicate if the related items should be loaded and added or not. Default is True
        @type recursive: bool
        @return: JSON representation of a user
        @rtype: String
        """
        out = dict()

        out["id"] = self.id
        out["username"] = self.username
        out["first_name"] = self.first_name
        out["last_name"] = self.last_name
        out["email"] = self.email
        out["tag"] = self.tag

        # if recursive is true we load the related parameters.
        if recursive:
            if self.UserProfile is None:
                out["profile"] = None
            else:
                out["profile"] = self.UserProfile.toJson()
        return out
