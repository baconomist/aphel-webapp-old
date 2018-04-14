import os

from modules.database_handler import DatabaseHandler
from modules.user import User
import logging
import hashlib, uuid
from flask import jsonify, request

import datetime


class RequestHandler(object):
    def __init__(self):
        # This is why this class needs an instance,
        # The app crashes if this dict is static
        self.functions = {"user_exists": DatabaseHandler.get_instance().user_exists,
                          "get_dashboard_data": self.dashboard, "get_new_announcement_id": self.get_new_announcement_id,
                            "get_announcements_for_user": self.get_announcements_for_user, "delete_announcement": self.delete_announcement}

    def handle_abstract(self):
        try:
            return jsonify(
                data=self.functions[request.get_json(force=True)["function"]](request.get_json(force=True)["data"]),
                status="Success")
        except:
            return jsonify(status="Error",
                           reason="Failed to execute abstract request!" +
                                  "\nNo matching function found: {function}".format(
                                      function=request.get_json(force=True)["function"]))

    def login(self):
        logging.info("self: Logging in...")
        assert request.method == "POST", b'The request method for login() was not "POST"!'
        data = request.get_json(force=True)
        result = self.do_login(data)
        logging.info(result)
        return result

    def signup(self):
        logging.info("self: Signing up...")
        assert request.method == "POST", b'The request method for signup() was not "POST"!'
        data = request.get_json(force=True)
        result = self.do_signup(data)
        logging.info(result)
        return result

    def do_signup(self, data):
        database = DatabaseHandler.get_instance()
        is_user_valid = self.is_userdata_valid(data["email"], data["password"])
        if "Success" in is_user_valid:
            database.store_user(User(data["email"], self.hash_password(data["password"])))
        return jsonify(status=is_user_valid)

    def do_login(self, data):
        print(data)
        for user in DatabaseHandler.get_instance().get_users():
            if user.uid == data["email"] and self.check_password(user.password, data["password"]):
                return jsonify(status="Logged in as %s" % user.uid, data=True)

        return jsonify(status="Failed to log in. The login credentials may be incorrect " \
                              "\n or the user does not exist.", data=False)

    def dashboard(self):
        return jsonify(data=DatabaseHandler.get_instance().get_announcements_json())

    def announcement(self):
        if self.is_user_logged_in():

            announcement_id = request.get_json(force=True)["data"]["announcement"]["id"]

            user = DatabaseHandler.get_instance().get_user(request.get_json(force=True)["data"]["login"]["email"])
            user.create_announcement(content_html=request.get_json(force=True)["data"]["announcement"]["content_html"],
                                     id=announcement_id)
            DatabaseHandler.get_instance().store_user(user)

            return jsonify(status="Success")
        else:
            return jsonify(status="Error")

    def is_user_admin(self):
        database = DatabaseHandler.get_instance()
        data = request.get_json(force=True)
        return database.get_user(data["email"]).get_permission_level() > 2

    def is_user_auth_for_post(self):
        database = DatabaseHandler.get_instance()
        data = request.get_json(force=True)
        return database.get_user(data["email"]).get_permission_level() > 1,

    def is_user_auth_for_post_review(self):
        database = DatabaseHandler.get_instance()
        data = request.get_json(force=True)
        return database.get_user(data["email"]).get_permission_level() > 0

    def user_exists(self):
        return DatabaseHandler.get_instance().user_exists(request.get_json(force=True)["data"])

    def get_new_announcement_id(self, user_id):
        return len(DatabaseHandler.get_instance().get_user(user_id).announcements) + 1

    def get_announcements_for_user(self, user_name):
        announcements = []
        for announcement in DatabaseHandler.get_instance().get_user(user_name).announcements:
            announcements.append(announcement.to_json())
        return announcements

    def delete_announcement(self, data):
        login = data["login"]
        announcement_id = data["announcement_id"]

        #if self.is_user_logged_in():


    def is_user_logged_in(self):
        return self.check_password(DatabaseHandler.get_instance().get_user(
            request.get_json(force=True)["data"]["login"]["email"]).password,
                            request.get_json(force=True)["data"]["login"]["password"])



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
