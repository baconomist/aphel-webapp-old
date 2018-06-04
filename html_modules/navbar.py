import os
from functools import wraps

from flask import session
from html_modules.html_module import HTML_Module
from modules.database_handler import DatabaseHandler
from cssutils import parseStyle


def admin(nav_function):
    @wraps(nav_function)
    def wrapper(*args, **kwargs):
        if session.get("uid") is None:
            return
        user = DatabaseHandler.get_instance().get_user(session.get("uid"))
        if user.permission_level >= user.get_teacher_permisison_level():
            return nav_function(*args, **kwargs)
        return None

    return wrapper


def auth_for_post(nav_function):
    @wraps(nav_function)
    def wrapper(*args, **kwargs):
        if session.get("uid") is None:
            return
        user = DatabaseHandler.get_instance().get_user(session.get("uid"))
        if user.permission_level >= user.get_untrusted_student_permission_level():
            return nav_function(*args, **kwargs)
        return None

    return wrapper


def not_logged_in(nav_function):
    @wraps(nav_function)
    def wrapper(*args, **kwargs):
        if session.get("uid") is None:
            return nav_function(*args, **kwargs)
        return None

    return wrapper


class Navbar(HTML_Module):
    def __init__(self):
        file = open(os.path.join(os.path.dirname(__file__), "navbar.html"), "r")
        file_data = file.read()
        file.close()

        super(Navbar, self).__init__(file_data)

        self.nav_user = self.bs4Obj.find(id="nav_user")
        self.nav_login = self.bs4Obj.find(id="nav_login")
        self.nav_register = self.bs4Obj.find(id="nav_register")

        self.update()

    def update(self):
        self.navbar_admin()
        self.navbar_post()
        self.navbar_not_logged_in()

    @admin
    def navbar_admin(self):
        for element in self.bs4Obj.find_all(class_="admin"):
            element["style"] = parseStyle(element["style"]).removeProperty("display")
        self.bs4Obj.find(id="nav_user")["style"] = parseStyle(self.nav_user["style"]).removeProperty("display")

    @auth_for_post
    def navbar_post(self):
        for element in self.bs4Obj.find_all(class_="auth-for-post"):
            element["style"] = parseStyle(element["style"]).removeProperty("display")
        try:
            self.nav_user["style"] = parseStyle(self.nav_user["style"]).removeProperty("display")
        except:
            pass

    @not_logged_in
    def navbar_not_logged_in(self):
        self.nav_login["style"] = parseStyle(
            self.nav_login["style"]).removeProperty("display")
        self.nav_register["style"] = parseStyle(
            self.nav_register["style"]).removeProperty("display")
