"""
Database Model File for a Exercise.
@author: mkaiser
"""
from .Base import Base
from .Subject import Subject
from sqlalchemy import String, Column, DateTime, Integer, func, \
    ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.orderinglist import ordering_list
from .Session import Session


class Exercise(Base):
    """
    Class that represents a exercise.
    Exercise holds multiple tasks (is a Group of tasks)
    """

    __tablename__ = 'exercise'

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
    # name of the task that is visible to users
    name = Column(
        String, nullable=False, index=True
    )
    # tag for filtering
    tag = Column(
        String, nullable=True
    )

    # Foreign Keys
    subject_id = Column(
        Integer,
        ForeignKey(Subject.id, onupdate="CASCADE"),
        nullable=True,
        index=True
    )

    tasks = relationship(
        "Task",
        collection_class=ordering_list("name"),
        order_by="[Task.name]",
        # cascade="all",
        passive_deletes=True,
        lazy="subquery",
        backref=backref("TaskExercise", lazy="joined")
    )

    def get_profile(self):
        if self.ExerciseSubject is None:
            return None
        else:
            return self.ExerciseSubject.get_profile()

    def toJson(self, recursive: bool = True) -> dict:
        """
        Render the json representation of a Task
        @param recursive: Parameter to indicate if the related items should be loaded and added or not. Default is True
        @type recursive: bool
        @return: JSON representation of a Task
        @rtype: dict
        """
        out = dict()
        out["id"] = self.id
        out["name"] = self.name
        out["tag"] = self.tag

        if recursive:
            if self.tasks is None:
                out["tasks"] = None
            else:
                _tasks = []
                for task in self.tasks:
                    _tasks.append(task.toJson())
                out["tasks"] = _tasks

            out["profile"] = self.get_profile()

            if self.subject_id is None:
                out["subject"] = None
            else:
                out["subject"] = self.ExerciseSubject.toJson(recursive=False)

        return out
