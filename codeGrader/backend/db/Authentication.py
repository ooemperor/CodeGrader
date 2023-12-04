"""
DB Model File that holds all the classes/tables that are related to the Authentication of the API
@author: mkaiser
"""
from .Base import Base
from sqlalchemy import String, Column, DateTime, Integer, func
from codeGrader.backend.config import config
import string
import random


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
    description = Column(
        String, nullable=False, index=False
    )

    def __init__(self, description: str) -> None:
        """
        API Token Constructor of an Object in the database
        Overwrites the Base Constructor.
        @param description: the description of the token and what it is used for.
        @type description: str
        """
        self.cls = type(self)  # cls is short form for class
        assert description is not None
        kwargs = dict()
        kwargs["description"] = description

        token = ""
        for i in range(0, config.tokenLength):
            token += random.choice(string.ascii_lowercase + string.digits)

        kwargs["token"] = token

        # after preprocessing setting/updating the attributes
        self.set_attrs(kwargs)
