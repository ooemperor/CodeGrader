"""
File for all the admin handlers
"""

from .Base import BaseHandler
from flask import Request, render_template, redirect, url_for
import flask


class AdminUserListHandler(BaseHandler):
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
        admins = self.api.get("/adminUsers")
        return render_template("adminUsers.html", **admins)


class AdminUserHandler(BaseHandler):
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
        print(admin_data)


        self.api.put(f"/adminUser/{id_}", body=admin_data)

        return redirect(url_for("adminUser", id_=id_))
