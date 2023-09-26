"""
Basic Database Object that all Tables do inherit from
@author: mkaiser
"""
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import String, Integer, Column, Boolean, Float, Enum, DateTime, Interval, BIGINT
from src.backend.config import config
from src.backend.db import dbEngine
from sqlalchemy.orm import \
    class_mapper, object_mapper, ColumnProperty, RelationshipProperty


@as_declarative()
class Base(object):
    """
    The dbBase (Database Base) class that defines the constructor and other functions for all objects on the database
    Inherits from the basic object class from python.
    """
    # Loading the amount of metadatacolumns
    # these are columsn that contain data, that only the database should manage
    # e.g. creation_dts and id (primary_key)
    metadatacolumns = config.metadataColumnsAmount

    def __init__(self, **kwargs):
        """
        Base Constructor of an Object in the database
        @param kwargs: multiple input keyword:arguments
        @type kwargs: dict
        @raise ValueError: when too many values are provided to the object
        """
        # to be defined if this is needed or not
        # check if we have more attributes than needed
        self.cls = type(self)  # cls is short form for class

        try:
            self._constructorInputCheck(kwargs)

        except Exception:
            raise ValueError("The attributes provided do not match with the attributes needed for the object")

        # after preprocessing setting/updating the attributes
        self.set_attrs(kwargs)

    @classmethod
    def __declare_last__(cls):
        """
        This function will run after all the
        @return:
        """
        cls.column_properties = list()
        cls.relationship_properties = list()

        for prop in class_mapper(cls).iterate_properties:
            if isinstance(prop, ColumnProperty):
                col = prop.columns[0]
                if col.primary_key or col.foreign_keys or col.name in config.columnIgnoreList:
                    continue

                cls.column_properties.append(prop)

            elif isinstance(prop, RelationshipProperty):
                cls.relationship_properties.append(prop)

    def _constructorInputCheck(self, **kwargs):
        """
        Checks if the amount of
        @param kwargs: dict with params as a key:value pair
        @type kwargs: dict
        @return: No return
        """
        if len(kwargs.keys()) > (len(self._col_props) - self.metadatacolumns):
            raise AttributeError("More values provided than the Class supports in its construction")

    def set_attrs(self, attributes, fill_with_defaults=True):
        """
        Setting the attributes for an object defined by the attributes
        @param attributes: values of the object that shall be set
        @type attributes: dict
        @param fill_with_defaults: If empty Columns shall be filled with the default values of the database
        @type fill_with_defaults: Boolean
        @return: No return for setter
        @rtype: None
        """
        # make deep copy of attributes, so we have a working dictionary
        # this way no changes to original input are made
        attributes = attributes.copy()

        # updating variables/columns of the object
        # TODO: needs cleaning and better error control
        for object_var in self.column_properties:
            column = object_var.columns[0]

            if object_var.key not in attributes and fill_with_defaults:
                # no data has been provided for this variable
                # must check if column can be null when no default is set.
                if column.default is None and column.nullable is False:
                    raise AttributeError(
                        "Columns is not nullable. No data data has been provided for the Variable '%s' and there is no default value"
                        % object_var.key
                    )
                setattr(self, object_var.key, column.default)

            elif object_var.key in attributes:
                value = attributes.pop(object_var.key)
                setattr(self, object_var.key, value)

            else:
                # no value specified or shall not fill with default
                if column.nullable is False:
                    raise AttributeError(
                        "Columns is not nullable. No data data has been provided for the Column '%s'" % object_var.key
                    )

        # updating the relationships
        for relationship in self.relationship_properties:
            if relationship.key in attributes:
                val = attributes.pop(relationship.key)

                setattr(self, relationship.key, val)

    def get_attrs(self):
        """
        Getting a dictionary of all the arguments for a given Object in the Database
        @return: The dictionary with the attributes and values that define the Object on which the function is called.
        @rtype: dict
        """
        data = dict()

        # go through all columns and add them to the data dictionary
        for val in self.column_properties:
            data[val.key] = getattr(val)
        return data
