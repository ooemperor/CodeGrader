"""
Database Model File for a TestCase to a given Task.
@author: mkaiser
"""

from .Base import Base
from .File import File
from .Task import Task
from sqlalchemy import String, Column, DateTime, Integer, func, \
    ForeignKey
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship, backref


class TestCase(Base):
    """
    TestCase for a given Task
    """

    __tablename__ = 'testcase'

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

    # the input for the TestCase
    # input can be null
    input_id = Column(
        ForeignKey(File.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    # the Output for the testcase
    # output cannot not be null
    output_id = Column(
        ForeignKey(File.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    task_id = Column(
        Integer,
        ForeignKey(Task.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )

    input_file = relationship(
        "File",
        foreign_keys=input_id,
        collection_class=ordering_list("id"),
        order_by="[File.id]",
        cascade="all",
        passive_deletes=True,
        lazy="joined"
    )

    # Relationships
    output_file = relationship(
        "File",
        foreign_keys=output_id,
        collection_class=ordering_list("id"),
        order_by="[File.id]",
        cascade="all",
        passive_deletes=True,
        lazy="joined"
    )

