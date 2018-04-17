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
        '''self.functions = {"user_exists": self.database.user_exists,
                          "get_dashboard_data": self.dashboard, "get_new_announcement_id": self.get_new_announcement_id,
                            "get_announcements_for_user": self.get_announcements_for_user, "delete_announcement": self.delete_announcement}'''

        self.request = {}
        self.request_data = {}
        self.request_function = ""

        self.database = DatabaseHandler.get_instance()

    def handle_request(self):
        self.request = request.get_json(force=True)
        try:
            self.request_data = self.request["data"]
        except:
            self.request_data = None

        self.request_function = self.request["function"]

        # Get function by name from class
        try:
            return getattr(self, self.request["function"])()
        # No matching function found
        except AttributeError as ae:
            print(ae, "Error, Failed to execute abstract request!" +
                                  "\nNo matching function found: {function}".format(function=self.request["function"]))
            return jsonify(status="Error, Failed to execute abstract request!" +
                                  "\nNo matching function found: {function}".format(function=self.request["function"]))
        # Function created an arbitrary error
        except Exception as e:
            print(e, "Error, Function call failed!")
            return jsonify(status="Error, Function call failed!")

    def login(self):
        logging.info("Request Handler: Logging in...")

        email = self.request_data["login"]["email"]
        password = self.request_data["login"]["password"]

        for user in self.database.get_users():
            if user.uid == email and self.check_password(user.password, password):
                logging.info("Logged in as %s" % user.uid)
                return jsonify(data=True, status="Logged in as %s" % user.uid)

        logging.info("Failed to log in. The login credentials may be incorrect "
                     "\n or the user does not exist.")
        return jsonify(data=False, status="Failed to log in. The login credentials may be incorrect "
                                          "\n or the user does not exist.")

    def signup(self):
        logging.info("Request Handler: Signing up...")

        email = self.request_data["login"]["email"]
        password = self.request_data["login"]["password"]

        is_user_valid = self.is_user_data_valid(email, password)

        if "Success" in is_user_valid:
            self.database.store_user(User(email, self.hash_password(password)))
            logging.info(is_user_valid)
            return jsonify(data=True, status=is_user_valid)

        logging.info(is_user_valid)

        return jsonify(data=False, status=is_user_valid)

    # **************************************************************************************************
    def get_dashboard(self):
        print("hi")
        return jsonify(data=self.database.get_announcements_json())

    # **************************************************************************************************

    def save_announcement(self):
        if self.is_user_logged_in():

            announcement_id = self.request_data["announcement"]["id"]

            user = self.database.get_user(self.request_data["login"]["email"])
            user.create_announcement(content_html=self.request_data["announcement"]["content_html"],
                                     id=announcement_id)
            self.database.store_user(user)

            return jsonify(status="Success", data=True)
        else:
            return jsonify(status="Error", data=False)

    def is_user_admin(self):
        return jsonify(data=self.database.get_user(self.request_data["login"]["email"]).get_permission_level() > 2)

    def is_user_auth_for_post(self):
        return jsonify(data=self.database.get_user(self.request_data["login"]["email"]).get_permission_level() > 1)

    def is_user_auth_for_post_review(self):
        return jsonify(data=self.database.get_user(self.request_data["login"]["email"]).get_permission_level() > 0)

    def user_exists(self):
        return jsonify(data=self.database.user_exists(self.request_data))

    def get_new_announcement_id(self):
        return jsonify(data=len(self.database.get_user(self.request_data["email"]).announcements) + 1)

    def get_announcements_for_user(self):
        user_name = self.request_data["email"]
        announcements = []
        for announcement in self.database.get_user(user_name).announcements:
            announcements.append(announcement.to_json())
        return jsonify(data=announcements)

    def delete_announcement(self):
        email = self.request_data["login"]["email"]
        announcement_id = self.request_data["announcement_id"]

        if self.is_user_logged_in():
            user = self.database.get_user(email)
            user.remove_announcement_by_id(announcement_id)
            self.database.store_user(user)
            return "Announcement deleted"
        return "User not logged in"

    def is_user_logged_in(self):
        return self.check_password(self.database.get_user(
            self.request_data["login"]["email"]).password,
                                   self.request_data["login"]["password"])

    '''
    Helper methods
    '''

    def is_user_data_valid(self, email, password):
        database = self.database

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
