"""
Basic Database Object that all Tables do inherit from
@author: mkaiser
"""

from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import String, Integer, Column, Boolean, Float, Enum, DateTime, Interval, BIGINT


@as_declarative()
class Base(object):
    """
    The dbBase (Database Base) class that defines the constructor and other functions for all objects on the database
    """
    def __init__(self, *args, **kwargs):
        """
        Base Constructor of an Object in the database
        @param args: multiple input arguments
        @param kwargs: multiple input keyword:arguments
        @raise: AttributeError when too many values are provided to the object
        """


        # check if
        if len(kwargs.keys()) > len(self._col_props):
            raise AttributeError("More values provided than Object supports")

        # might wanna catch the error here
        self.set_attrs(kwargs)



    def set_attrs(self, attributes, fill_with_defaults=True):
        """
        Setting the attributes for a object defined by the attributes
        @param attributes: the attributes of the object that shall be set
        @type attributes: Dictionary
        @param fill_with_defaults: If empty Columns shall be filled with the default values of the database
        @type fill_with_defaults: Boolean
        @return: True of successful, false if error
        """
        # attributes = attributes.copy()
        # TODO: implement function
        return True


    def get_attrs(self):
        """
        Getting a dictionary of all the arguments for a given Object in the Database
        @return: The dictionary with the attributes and values that define the Object on which the function is called.
        """
        data = dict()

        # go through all columns and add them to the data dictionary
        for val in self._col_props:
            data[val.key] = getattr(val)

        return data
