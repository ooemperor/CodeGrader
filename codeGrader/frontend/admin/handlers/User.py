"""
Handler Classes for the Users in the admin frontend
@author: mkaiser
"""
import flask
from flask import render_template, redirect, url_for, Response
from .Base import BaseHandler
from typing import Union


class UserListHandler(BaseHandler):
    """
    Handles Operations for the Users site
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the Users Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self) -> str:
        """
        Renders the template for the Users site.
        @return: The rendered template
        @rtype: HTML
        """
        users = self.api.get("/users", profile=self.admin.get_filter_profile())
        return render_template("users.html", **users, this=self)


class UserHandler(BaseHandler):
    """
    Handles the operation on a single User
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the User Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get and render the page for a given user by its id
        @param id_: The id of the user
        @type id_: int
        @return: The rendered page of the user
        @rtype: HTML
        """

        user = self.api.get(f"/user/{id_}")  # get the user data
        profiles = self.api.get(f"/profiles", name=self.admin.get_filter_profile_name())  # get the profile data

        user["profiles"] = profiles["profile"]

        # checking if user will be able to edit the table
        editable = self.admin.check_permission('w', user["profile"]["name"])

        user["editable"] = editable

        if self.admin.check_permission('r', user["profile"]["name"]):  # when admin is allowed to view this user
            return render_template("user.html", **user)

        else:  # admin is not allowed to view this user
            self.flash("You are not allowed to view this user. ")
            return redirect(url_for("users"))

    def post(self, id_: int) -> Response:
        """
        Handler for the update of a user
        @param id_:
        @param data:
        @return:
        """
        assert self.request.form is not None

        user_before = self.api.get(f"/user/{id_}")  # get the user data
        if self.admin.check_permission('w', user_before["profile"]["name"]):
            user_data = dict()

            # getting the data from the form provided in the request
            user_data["username"] = self.get_value("username")
            user_data["first_name"] = self.get_value("first_name")
            user_data["last_name"] = self.get_value("last_name")
            user_data["email"] = self.get_value("email")
            user_data["tag"] = self.get_value("tag")

            user_data["profile_id"] = self.get_value("profile")

            self.api.put(f"/user/{id_}", body=user_data)

        else:
            self.flash("You are not allowed to update this user! ")

        # either way, return the user to the user
        return redirect(url_for("user", id_=id_))


class AddUserHandler(BaseHandler):
    """
    Handler Class for the creation of an user
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the AddUser Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self) -> Union[str, Response]:
        """
        Get and render the site to create an admin user
        @return: The rendered page.
        """
        if self.admin.check_permission('w', 'user'):

            user_data = dict()

            profiles = self.api.get(f"/profiles", name=self.admin.get_filter_profile_name())
            user_data["profiles"] = profiles["profile"]

            return render_template("addUser.html", **user_data)

        else:  # admin is not allowed to view this user
            self.flash("You are not allowed to access this site! ")
            return redirect(url_for("users"))

    def post(self) -> Response:
        """
        Post Operation
        Creates the admin user specified by the parameters in the backend.
        @return: Redirect to the adminUsers Site
        """
        assert self.request.form is not None

        if self.admin.check_permission('w', create_object='user'):
            user_data = dict()

            # getting the data from the form provided in the request
            user_data["username"] = self.get_value("username")
            user_data["first_name"] = self.get_value("first_name")
            user_data["last_name"] = self.get_value("last_name")
            user_data["email"] = self.get_value("email")
            user_data["tag"] = self.get_value("tag")
            user_data["password"] = self.get_value("password")

            user_data["profile_id"] = self.get_value("profile")

            self.api.post(f"/user/add", body=user_data)

        else:
            self.flash("You are not allowed to view this site. ")

        # either way redirect to the users page.
        return redirect(url_for("users"))


class DeleteUserHandler(BaseHandler):
    """
    Handler to delete a user from the api backend
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the DeleteUserHandler Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get Handler to render the site for confirmation for deletion of an user
        @param id_: The id_ of the user
        @type id_: int
        @return: Rendered Template
        """

        user = self.api.get(f"/user/{id_}")

        editable = self.admin.check_permission('w', user["profile"]["name"])

        if editable:
            return render_template("deleteUser.html", **user)

        else:
            self.flash("You are not allowed to delete users. ")
            return redirect(url_for("users"))

    def post(self, id_: int) -> Response:
        """
        Post Operation for User Deletion
        Deletes the user in the backend via an API Call
        @param id_: The identifier of the user
        @type id_: int
        @return: Redirection to the users table
        """
        user = self.api.get(f"/user/{id_}")
        if self.admin.check_permission('w', user["profile"]["name"]):  # admin is allowed to delete the user

            if self.get_value("action_button") == "Submit":
                self.api.delete(f"/user/{id_}")

                # display message that user has been deleted on the returned page.
                self.flash("User has been deleted")
                return redirect(url_for("users"))

            elif self.get_value("action_button") == "Cancel":
                return redirect(url_for("user", id_=id_))

            else:
                self.flash("You made an illegal operation. Please Try Again or Contact an Administrator!")
                return redirect(url_for("user", id_=id_))

        else:  # admin is not allowed to delete users
            self.flash("You are not allowed to delete users. ")
            return redirect(url_for("users"))
