"""
Basic Database Object that all Tables do inherit from
@author: mkaiser
"""
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, Column, Boolean, Float, Enum, DateTime, Interval, BIGINT


class Base(DeclarativeBase):
    """
    The dbBase (Database Base) class that defines the constructor and other functions for all objects on the database
    """
    def __init__(self, *args, **kwargs):
        """
        Base Constructor of a Object in the database
        @param args: multiple input arguments
        @param kwargs: multiple input keyword:arguments
        """

    def set_attrs(self, attributes, fill_with_defaults=True):
        """

        @param attributes: the attributes of the object that shall be set
        @param fill_with_defaults: If empty Columns shall be filled with the default values of the database
        @return: True of successful, false if error
        """
        attributes = attributes.copy()
        # TODO: implement function
        return True

    def get_attrs(self):
        """
        Getting a dictionary of all the arguments for a given Object in the Database
        @return: The dictionary with the attributes.
        """
        # TODO: implement function