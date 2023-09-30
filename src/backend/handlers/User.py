"""
Holds the Handlers for everything that corresponds with the Users
@author: mkaiser
# TODO: Handle Errors while parsing information or querying the database
# TODO: Define and document proper response after put and post operations.
# TODO: Define how to handle realtions of Profile and more.

"""
from src.backend.handlers.Base import BaseHandler
from src.backend.db import User, AdminUser


class UserHandler(BaseHandler):
    """
    Handler for a UserObject
    """
    def get(self, id_):
        """
        Get a specific AdminUser from the database
        @param id_: the id of the user in the database
        @type id_: int
        @return: JSON representation of the object
        @rtype: str
        """

        assert (id_ is not None) and (id_ > 0)

        super().__init__()

        with self.sql_session.session.begin() as sql:
            user = sql.get(User, id_)
            sql.expunge(user)  # taking the user away from the session, so we can work on it away from DB.

        assert user is not None
        return user.get_attrs()  # TODO: need to make better user representation.

    def post(self, dict_):
        """
        Creating a new user object and writing in the database
        @param dict_: The dictionary/ key:value pair for the creation of the user
        @type dict_: dict
        @return: True else Error # TODO: Add more meaningful return Type
        @rtype: Boolean
        """
        assert dict_ is not None
        assert len(dict_.keys()) == 6

        super().__init__()
        user = User(**dict_)
        new_user_id = self.sql_session.create(user)

        return f"{new_user_id}"  # TODO: Return has to be more precise

    def put(self, id_, dict_):
        """
        Updating a existing user in the database
        @param id_: The identifier of the object
        @type id_: int
        @param dict_: the arguments for the user that are updated
        @type dict_: key:value pairs
        @return: True or False depending on the outcome of the post. # TODO: will be further refined
        @rtype: Boolean
        """
        assert (id_ is not None) and (id_ > 0)
        assert dict_ is not None
        assert len(dict_.keys()) == 6

        super().__init__()
        self.sql_session.update(User, id_, dict_)
        return "Updated"

    def delete(self, id_):
        """
        Deleting a user from the database
        @param id_: The identifier of the object
        @type id_: int
        @return: True or False depending on the outcome of the post. # TODO: will be further refined
        @rtype: Boolean
        """
        assert (id_ is not None) and (id_ > 0)

        super().__init__()

        self.sql_session.delete(User, id_)
        return "True"


class AdminUserHandler(BaseHandler):
    """
    Handler for the AdminUser
    """
    def get(self, id_):
        """
        Get a specific AdminUser from the database
        @param id_: the id of the user in the database
        @type id_: int
        @return: JSON representation of the object
        @rtype: str
        """
        # TODO: Require source of origin to be the adminFrontend
        assert (id_ is not None) and (id_ > 0)
        super().__init__()

        with self.sql_session.session.begin() as sql:
            admin = sql.get(AdminUser, id_)
            sql.expunge(admin)  # taking the user away from the session, so we can work on it away from DB.

        assert admin is not None
        return admin.get_attrs()  # TODO: need to make better user representation.

    def post(self, dict_):
        """
        Creating a new AdminUser object and writing in the database
        @param dict_: The dictionary/ key:value pair for the creation of the user
        @type dict_: dict
        @return: True else Error # TODO: Add more meaningful return Type
        @rtype: Boolean
        """
        # TODO: Require source of origin to be the adminFrontend
        super().__init__()
        admin = AdminUser(**dict_)
        new_user_id = self.sql_session.create(admin)

        return f"{new_user_id}"  # TODO: Return has to be more precise

    def put(self, id_, dict_):
        """
        Updating a existing Adminuser in the database
        @param id_: The identifier of the object
        @type id_: int
        @param dict_: the arguments for the user that are updated
        @type dict_: key:value pairs
        @return: True or False depending on the outcome of the post. # TODO: will be further refined
        @rtype: Boolean
        """
        # TODO: Require source of origin to be the adminFrontend
        super().__init__()
        self.sql_session.update(AdminUser, id_, dict_)
        return "Updated"

    def delete(self, id_):
        """
        Deleting a Adminuser from the database
        @param id_: The identifier of the object
        @type id_: int
        @return: True or False depending on the outcome of the post. # TODO: will be further refined
        @rtype: Boolean
        """
        # TODO: Require source of origin to be the adminFrontend
        super().__init__()

        self.sql_session.delete(AdminUser, id_)
        return "True"




