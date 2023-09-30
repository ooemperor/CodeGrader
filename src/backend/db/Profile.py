"""
Database Model File for storing all the profiles that we are using. This introduces the capability to later on filter by profile
@author: mkaiser
"""
from src.backend.db.Base import Base
from sqlalchemy import String, Integer, Column, Boolean, Float, Enum, DateTime, Interval, BIGINT, VARCHAR, func
from sqlalchemy.orm import relationship
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
        cascade="all",
        passive_deletes=True,
        backref="UserProfile"
    )

    # relationship to the adminusers
    adminUsers = relationship(
        "AdminUser",
        collection_class=ordering_list("username"),
        order_by="[AdminUser.username]",
        cascade="all",
        passive_deletes=True,
        backref="AdminUserProfile"
    )

    #relationships to the subjects
    subjects = relationship(
        "Subject",
        collection_class=ordering_list("name"),
        order_by="[Subject.name]",
        cascade="all",
        passive_deletes=True,
        backref="SubjectProfile"
    )

