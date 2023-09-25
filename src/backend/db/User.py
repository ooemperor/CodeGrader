"""
Database Model File for a user with its given column properties.
@author: mkaiser
"""
from src.backend.db.Base import Base
from sqlalchemy import String, Integer, Column, Boolean, Float, Enum, DateTime, Interval, BIGINT, VARCHAR, func, \
    ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list
from src.backend.db.Profile import Profile


class User(Base):
    """
    Class to represent a User in the database
    @see: db.Base
    """

    __tablename__ = "user"
    # primary key
    id = Column(
        BIGINT, primary_key=True
    )
    # Datetimestamp of creation in the database
    creation_dts = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
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
        String, nullable=False
    )
    # usertag for filtering
    tag = Column(
        String, nullable=True
    )
    # Foreign Keys
    # Foreign key to the Profile Table
    profile_id = Column(
        BIGINT, ForeignKey(Profile.id, onupdate="CASCADE", ondelete="CASCADE"), nullable=True, index=True
    )


class AdminUser(Base):
    """
    Class to store all the administrator users
    """
    __tablename__ = 'adminuser'
    # primary key
    id = Column(
        BIGINT, primary_key=True
    )
    creation_dts = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
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
        String, nullable=False
    )
    # usertag for filtering
    tag = Column(
        String, nullable=True
    )

    # Foreign key to the Profile Table
    profile_id = Column(
        BIGINT,
        ForeignKey(Profile.id, onupdate="CASCADE", ondelete="CASCADE"),
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
        backref="Membership"
    )