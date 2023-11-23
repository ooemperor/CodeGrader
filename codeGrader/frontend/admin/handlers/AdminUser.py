"""
File for all the admin handlers
"""

from .Base import BaseHandler
from flask import Request, render_template, redirect, url_for
import flask


class AdminListHandler(BaseHandler):
    """
    Handles Operations for the Users site
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the AdminUserList Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self):
        """
        Renders the template for the Users site.
        @return: The rendered template
        @rtype: HTML
        """
        admins = self.api.get("/admins")
        return render_template("adminUsers.html", **admins)


class AdminHandler(BaseHandler):
    """
    Handles the operation on a single adminuser
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the AdminUser Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self, id_: int):
        """
        Get and render the page for a given AdminUser by its id
        @param id_: The id of the AdminUser
        @type id_: int
        @return: The rendered page of the AdminUser
        @rtype: HTML
        """
        admin = self.api.get(f"/adminUser/{id_}")

        admin_types = self.api.get(f"/adminTypes")
        admin["types"] = admin_types["admin_type"]

        profiles = self.api.get(f"/profiles")
        admin["profiles"] = profiles["profile"]

        return render_template("adminUser.html", **admin)

    def post(self, id_: int):
        """
        Handler for the update of a AdminUser
        @param id_: The id of the admin user in the database
        @type id_: int
        @return: Redirect to the correct adminUser page.
        """

        assert self.request.form is not None
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

        return redirect(url_for("adminUser", id_=id_))


class AddAdminHandler(BaseHandler):
    """
    Handler Class for the creation of an admin user
    """

    def __init__(self, request: flask.Request):
        """
        Constructor of the AddAdminUser Handler
        @param request: The request from the app route of flask
        @type request: flask.Request
        """
        super().__init__(request)

    def get(self):
        """
        Get and render the site to create an admin user
        @return: The rendered page.
        """
        admin_data = dict()

        admin_types = self.api.get(f"/adminTypes")
        admin_data["types"] = admin_types["admin_type"]

        profiles = self.api.get(f"/profiles")
        admin_data["profiles"] = profiles["profile"]

        return render_template("addAdminUser.html", **admin_data)

    def post(self):
        """
        Post Operation
        Creates the admin user specified by the parameters in the backend.
        @return: Redirect to the adminUsers Site
        """

        assert self.request.form is not None
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

        return redirect(url_for("admins"))
