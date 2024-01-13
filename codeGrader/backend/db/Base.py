# CodeGrader - https://github.com/ooemperor/CodeGrader
# Copyright © 2023, 2024 Michael Kaiser <michael.kaiser@emplabs.ch>
#
# This file is part of CodeGrader.
#
# CodeGrader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CodeGrader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CodeGrader.  If not, see <http://www.gnu.org/licenses/>.

"""
Basic Database Object that all Tables do inherit from
@author: mkaiser
"""
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy import Boolean
from codeGrader.backend.config import config
from sqlalchemy.orm import \
    class_mapper, ColumnProperty, RelationshipProperty


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

    def __init__(self, **kwargs) -> None:
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
    def __declare_last__(cls) -> None:
        """
        This function will run after all the
        @return:
        """
        cls.column_properties = list()
        cls.relationship_properties = list()

        for prop in class_mapper(cls).iterate_properties:
            if isinstance(prop, ColumnProperty):
                col = prop.columns[0]
                if col.primary_key or col.name in config.columnIgnoreList:
                    continue

                cls.column_properties.append(prop)

            elif isinstance(prop, RelationshipProperty):
                cls.relationship_properties.append(prop)

    def _constructorInputCheck(self, **kwargs) -> None:
        """
        Checks if the amount of
        @param kwargs: dict with params as a key:value pair
        @type kwargs: dict
        @return: No return
        """
        if len(kwargs.keys()) > (len(self.column_properties) - self.metadatacolumns):
            raise AttributeError("More values provided than the Class supports in its construction")

    def set_attrs(self, attributes: dict, fill_with_defaults=True) -> None:
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
                attr = object_var.key
                if column.default is None and column.nullable is False and getattr(self, object_var.key) is None:
                    raise AttributeError(
                        "Columns is not nullable. No data data has been provided for the Variable '%s' and there is no default value"
                        % object_var.key
                    )
                elif getattr(self, object_var.key) is not None:
                    continue
                else:
                    setattr(self, object_var.key, column.default)

            elif object_var.key in attributes:
                value = attributes.pop(object_var.key)
                setattr(self, object_var.key, value)

            else:
                # no value specified or shall not fill with default

                if getattr(self, object_var.key) is not None:
                    continue
                else:
                    if column.nullable is False:
                        raise AttributeError(
                            "Columns is not nullable. No data data has been provided for the Column '%s'" % object_var.key
                        )

        # updating the relationships
        for relationship in self.relationship_properties:
            if relationship.key in attributes:
                val = attributes.pop(relationship.key)

                setattr(self, relationship.key, val)

    def get_attrs(self) -> dict:
        """
        Getting a dictionary of all the arguments for a given Object in the Database
        This representation contains every column, including columns such as foreign keys and more.
        @return: The dictionary with the attributes and values that define the Object on which the function is called.
        @rtype: dict
        """
        data = dict()

        # go through all columns and add them to the data dictionary
        for val in self.column_properties:
            data[val.key] = getattr(self, val.key)
        return data

