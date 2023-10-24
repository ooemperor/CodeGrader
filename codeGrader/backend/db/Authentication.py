"""
DB Model File that holds all the classes/tables that are related to the Authentication of the API
@author: mkaiser
"""
from .Base import Base
from sqlalchemy import String, Column, DateTime, Integer, func


class APIToken(Base):
    """
    Class that represents a exercise.
    Exercise holds multiple tasks (is a Group of tasks)
    """

    __tablename__ = 'token'

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

    #the token will be in form of a hash
    token = Column(
        String, nullable=False, index=True
    )
    owner = Column(
        String, nullable=False, index=False
    )
