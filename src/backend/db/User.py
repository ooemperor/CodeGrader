"""
Database Model File for a user with its given column properties.
@author: mkaiser
"""
from src.backend.db.Base import Base
from sqlalchemy import String, Integer, Column, Boolean, Float, Enum, DateTime, Interval, BIGINT


class User(Base):
    """
    Class to represent a User in the database
    @see: db.Base
    """

    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)


