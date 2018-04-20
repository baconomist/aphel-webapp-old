import os

from modules.database_handler import DatabaseHandler
from modules.user import User
from modules.confirmation_manager import ConfirmationManager
from modules.emailer import send_email
from modules.server import Server

import traceback

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
            print("\t**Error, Failed to execute abstract request!**" +
                  "\nNo matching function found: {function}".format(function=self.request["function"]))
            traceback.print_exc()
            return jsonify(status="Error, Failed to execute abstract request!" +
                                  "\nNo matching function found: {function}".format(function=self.request["function"]))
        # Function created an arbitrary error
        except Exception as e:
            print("\t**Error, Function call failed!**")
            traceback.print_exc()
            return jsonify(status="Error, Function call failed!")

    def login(self):
        logging.info("Request Handler: Logging in...")

        email = self.request_data["login"]["email"]
        password = self.request_data["login"]["password"]

        print(email, password)

        for user in self.database.get_users():
            if user.confirmed and user.uid == email and Helper.check_password(user.password, password):
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

        is_user_valid = Helper.is_user_data_valid(email, password)

        if "Success" in is_user_valid:
            user = User(email, Helper.hash_password(password))

            id = str(ConfirmationManager.get_instance().new_confirmation(user).id)

            send_email(receivers=email, subject="APHEL TECH EMAIL CONFIRMATION",
                       body=r"url: {server_ip}/confirmation?id={id}".format(server_ip=Server.ip, id=id))

            self.database.store_user(user)

            logging.info(is_user_valid)

            return jsonify(data=True, status=is_user_valid)

        logging.info(is_user_valid)

        return jsonify(data=False, status=is_user_valid)

    # **************************************************************************************************
    def get_dashboard(self):
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

    def validate_confirmation(self):
        confirmation_id = self.request_data["confirmation_id"]
        logging.info("Validating confirmation link...")
        return jsonify(data=ConfirmationManager.get_instance().validate_confirmation(confirmation_id))

    def is_user_logged_in(self):
        return self.database.get_user(self.request_data["login"]["email"].uid).confirmed and \
                   Helper.check_password(self.database.get_user(self.request_data["login"]["email"]).password,
                                     self.request_data["login"]["password"])\




class Helper(object):
    @staticmethod
    def is_user_data_valid(email, password):
        database = DatabaseHandler.get_instance()

        if not database.user_exists(email) and len(password) >= 8 and "@pdsb.net" in email:
            return "Successfully signed up %s" % email
        elif len(password) < 8:
            return "Failed to sign up! Password has to be >= 8  characters in length"
        elif not "@pdsb.net" in email:
            return "Failed to signup! You must use your @pdsb.net email!"
        else:
            return "Failed to sign up! User %s already exists!" % email

    @staticmethod
    def hash_password(password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    @staticmethod
    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    @staticmethod
    def is_user_admin(user):
        return user.get_permission_level() > 2

    @staticmethod
    def is_user_auth_for_post(user):
        return user.get_permission_level() > 1

    @staticmethod
    def is_user_auth_for_post_review(user):
        return user.get_permission_level() > 0
