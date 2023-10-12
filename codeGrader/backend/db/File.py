"""
Database Model to store a File (Attachment or Submission and more).
@author: mkaiser
"""
from codeGrader.backend.db.Base import Base
from sqlalchemy import String, Integer, Column, Boolean, Float, Enum, DateTime, Interval, BIGINT, VARCHAR, func, \
    LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.orderinglist import ordering_list


class File(Base):
    """
    Class to store a file in the database
    """
    __tablename__ = "file"
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
    filename = Column(
        String, nullable=False, index=True
    )
    # the file type. e.g .pdf, .py and more
    fileExtension = Column(
        String, nullable=False
    )
    #  the file directly in the database, not beautiful but worth a test
    file = Column(
        LargeBinary, nullable=False
    )

    def toJson(self):
        out = dict()
        out["filename"] = self.filename
        out["fileExtension"] = self.fileExtension
        out["file"] = self.file
        return out
