"""
Database Model File for a Task with its given column properties.
@author: mkaiser
"""
from src.backend.db.Base import Base
from sqlalchemy import String, Integer, Column, Boolean, Float, Enum, DateTime, Interval, BIGINT

class Task(Base):
    """
    Class to represent a Task in the database
    @see: db.Base
    """
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
