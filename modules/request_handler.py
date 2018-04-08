import os

from modules.database_handler import DatabaseHandler
from modules.user import User
import logging
import hashlib, uuid
from flask import jsonify, request


class RequestHandler(object):
    def __init__(self):
        # This is why this class needs an instance,
        # The app crashes if this dict is static
        self.functions = {"user_exists": DatabaseHandler.get_instance().user_exists,
                          "get_dashboard_data": self.dashboard}

    def handle_abstract(self):
        try:
            return jsonify(data=self.functions[request.form.get("function")](request.form.get("data")),
                           status="Success")
        except:
            return jsonify(status="Error",
                           reason="Failed to execute abstract request!" +
                                  "\nNo matching function found: {function}".format(function=request.form.get("function")))

    def login(self):
        logging.info("self: Logging in...")
        assert request.method == "POST", b'The request method for login() was not "POST"!'
        data = request.form
        result = self.do_login(data)
        logging.info(result)
        return result

    def signup(self):
        logging.info("self: Signing up...")
        assert request.method == "POST", b'The request method for signup() was not "POST"!'
        data = request.form
        result = self.do_signup(data)
        logging.info(result)
        return result

    def do_signup(self, data):
        database = DatabaseHandler.get_instance()
        is_user_valid = self.is_userdata_valid(data.get("email"), data.get("password"))
        if "Success" in is_user_valid:
            database.store_user(User(data.get("email"), self.hash_password(data.get("password"))))
        return jsonify(status=is_user_valid)

    def do_login(self, data):
        for user in DatabaseHandler.get_instance().get_users():
            if user.name == data.get("email") and self.check_password(user.password, data.get("password")):
                return jsonify(status="Logged in as %s" % user.name, data=True)

        return jsonify(status="Failed to log in. The login credentials may be incorrect " \
               "\n or the user does not exist.", data=False)

    def dashboard(self):
        try:
            file = open(os.path.join(__file__, "..\\..\\data\\dashboard.html"), "r")
            dashboard = file.read()
            file.close()
            print(dashboard)
            return jsonify(data=dashboard)
        except:
            print("b")
            return jsonify(data="")

    def announcement(self):

        announcement_data = request.form.get("data")

        dashboard = open(os.path.join(__file__, "..\\..\\data\\dashboard.html"), "w")
        dashboard.write(announcement_data)
        dashboard.close()

        return jsonify(status="Success")

    def is_user_admin(self):
        database = DatabaseHandler.get_instance()
        data = request.form
        return database.get_user(data.get("email")).get_permission_level() > 2

    def is_user_auth_for_post(self):
        database = DatabaseHandler.get_instance()
        data = request.form
        return database.get_user(data.get("email")).get_permission_level() > 1,

    def is_user_auth_for_post_review(self):
        database = DatabaseHandler.get_instance()
        data = request.form
        return database.get_user(data.get("email")).get_permission_level() > 0

    def user_exists(self):
        return DatabaseHandler.get_instance().user_exists(request.form.get("data"))

    '''
    Helper methods
    '''

    def is_userdata_valid(self, email, password):
        database = DatabaseHandler.get_instance()

        if not database.user_exists(email) and len(password) >= 8 and "@pdsb.net" in email:
            return "Successfully signed up %s" % email
        elif len(password) < 8:
            return "Failed to sign up! Password has to be >= 8  characters in length"
        elif not "@pdsb.net" in email:
            return "Failed to signup! You must use your @pdsb.net email!"
        else:
            return "Failed to sign up! User %s already exists!" % email

    def hash_password(self, password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    def check_password(self, hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
