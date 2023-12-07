"""
File for all the admin handlers
"""

from .Base import BaseHandler
from flask import render_template, redirect, url_for, flash, Response
import flask
from typing import Union


class AdminListHandler(BaseHandler):
    """
    Handles Operations for the Users site
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the AdminUserList Handler
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
        admins = self.api.get("/admins", profile=self.admin.get_filter_profile())
        return render_template("adminUsers.html", **admins, this=self)


class AdminHandler(BaseHandler):
    """
    Handles the operation on a single adminuser
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the AdminUser Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get and render the page for a given AdminUser by its id
        @param id_: The id of the AdminUser
        @type id_: int
        @return: The rendered page of the AdminUser
        @rtype: HTML
        """
        admin = self.api.get(f"/admin/{id_}")

        admin_types = self.api.get(f"/adminTypes")
        admin["types"] = admin_types["admin_type"]

        profiles = self.api.get(f"/profiles", name=self.admin.get_filter_profile_name())
        admin["profiles"] = profiles["profile"]

        editable = self.admin.check_permission('w')
        admin["editable"] = editable

        if self.admin.check_permission('r', admin["profile"]["name"]):  # when admin is allowed to view this admin
            return render_template("adminUser.html", **admin)

        else:  # admin is not allowed to view this user
            self.flash("You are not allowed to view this admin. ")
            return redirect(url_for("admins"))

    def post(self, id_: int) -> Response:
        """
        Handler for the update of a AdminUser
        @param id_: The id of the admin user in the database
        @type id_: int
        @return: Redirect to the correct adminUser page.
        """
        assert self.request.form is not None

        admin_before = self.api.get(f"/admin/{id_}")  # get the admin data
        if self.admin.check_permission('w', admin_before["profile"]["name"]):
            admin_data = dict()

            # getting the data from the form provided in the request
            admin_data["username"] = self.get_value("username")
            admin_data["first_name"] = self.get_value("first_name")
            admin_data["last_name"] = self.get_value("last_name")
            admin_data["email"] = self.get_value("email")
            admin_data["tag"] = self.get_value("tag")
            admin_data["admin_type"] = self.get_value("admin_type")

            admin_data["profile_id"] = self.get_value("profile")

            self.api.put(f"/admin/{id_}", body=admin_data)

        else:
            self.flash("You are not allowed to update this admin! ")

        return redirect(url_for("admin", id_=id_))


class AddAdminHandler(BaseHandler):
    """
    Handler Class for the creation of an admin user
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the AddAdminUser Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self) -> Union[str, Response]:
        """
        Get and render the site to create an admin user
        @return: The rendered page.
        """
        if self.admin.check_permission('w', 'admin'):

            admin_data = dict()

            admin_types = self.api.get(f"/adminTypes")
            admin_data["types"] = admin_types["admin_type"]

            profiles = self.api.get(f"/profiles", name=self.admin.get_filter_profile_name())
            admin_data["profiles"] = profiles["profile"]

            return render_template("addAdminUser.html", **admin_data)

        else:  # admin is not allowed to see this admin add page
            self.flash("You are not allowed to access this site")
            return redirect(url_for("admins"))

    def post(self) -> Response:
        """
        Post Operation
        Creates the admin user specified by the parameters in the backend.
        @return: Redirect to the adminUsers Site
        """

        assert self.request.form is not None

        if self.admin.check_permission('w', create_object='admin'):
            admin_data = dict()

            # getting the data from the form provided in the request
            admin_data["username"] = self.get_value("username")
            admin_data["first_name"] = self.get_value("first_name")
            admin_data["last_name"] = self.get_value("last_name")
            admin_data["email"] = self.get_value("email")
            admin_data["tag"] = self.get_value("tag")
            admin_data["admin_type"] = self.get_value("admin_type")
            admin_data["password"] = self.get_value("password")

            admin_data["profile_id"] = self.get_value("profile")

            self.api.post(f"/admin/add", body=admin_data)

        else:  # viewing this is not allowed
            self.flash("You are not allowed to view this site. ")

        # redirect either way
        return redirect(url_for("admins"))


class DeleteAdminHandler(BaseHandler):
    """
    Handler to delete a Task from the api backend
    """

    def __init__(self, request: flask.Request) -> None:
        """
        Constructor of the DeleteAdminHandler Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int) -> Union[str, Response]:
        """
        Get Handler to render the site for confirmation for deletion of an Admin
        @param id_: The id_ of the Admin
        @type id_: int
        @return: Rendered Template
        """
        admin = self.api.get(f"/admin/{id_}")

        editable = self.admin.check_permission('w')
        if editable:
            return render_template("deleteAdmin.html", **admin)

        else:
            self.flash("You are not allowed to delete admins. ")
            return redirect(url_for("admins"))

    def post(self, id_: int) -> Response:
        """
        Post Operation for Admin Deletion
        Deletes the task in the backend via an API Call
        @param id_: The idnentifier of the Admin
        @type id_: int
        @return: Redirection to the Admin table
        """

        admin = self.api.get(f"/admin/{id_}")
        if self.admin.check_permission('w', admin["profile"]["name"]):  # admin is allowed to delete the admin
            if self.get_value("action_button") == "Submit":
                self.api.delete(f"/admin/{id_}")

                # display message that Admin has been deleted on the returned page.
                flash("Admin has been deleted")
                return redirect(url_for("admins"))

            elif self.get_value("action_button") == "Cancel":
                return redirect(url_for("admin", id_=id_))

            else:
                pass
                # TODO Implement Error

        else:  # admin is not allowed to delete users
            self.flash("You are not allowed to delete admins. ")
            return redirect(url_for("admins"))
