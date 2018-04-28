import os

from modules.database_handler import DatabaseHandler
from modules.confirmation_manager import ConfirmationManager
from modules.announcement_review_handler import AnnouncementReviewHandler

from modules.user import User
from modules.teacher import Teacher


from modules.announcement import Announcement

from modules.emailer import send_email
from modules.server import Server

import traceback

import logging
import hashlib, uuid
from flask import jsonify, request

import datetime

''' ATTENTION '''
''' ALL METHODS IN REQUEST HANDLER ARE CALLABLE BY CLIENT '''
''' MAKE SURE THE METHODS HERE ARE SECURE '''
''' ATTENTION '''
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

            if Helper.is_teacher_email(email):
                user = Teacher(email, Helper.hash_password(password))
            else:
                user = User(email, Helper.hash_password(password))

            id = str(ConfirmationManager.get_instance().new_confirmation(user).id)

            send_email(receivers=email, subject="APHEL TECH EMAIL CONFIRMATION",
                       body=r"url: {server_ip}/confirmation_confirmed?id={id}".format(server_ip=Server.ip, id=id))

            self.database.store_user(user)

            logging.info(is_user_valid)

            return jsonify(data=True, status=is_user_valid)

        logging.info(is_user_valid)

        return jsonify(data=False, status=is_user_valid)

    def get_dashboard(self):
        return jsonify(data=self.database.get_announcements_json())

    def save_announcement(self):
        if self.is_user_logged_in() and Helper.is_user_auth_for_post(DatabaseHandler.get_instance().get_user(self.request_data["login"]["email"])):
            title = self.request_data["announcement_data"]["title"]
            info = self.request_data["announcement_data"]["info"]
            content_html = self.request_data["announcement_data"]["content_html"]
            id = self.request_data["announcement_data"]["id"]

            user = self.database.get_user(self.request_data["login"]["email"])
            user.create_announcement(title=title, info=info, content_html=content_html, id=id)
            self.database.store_user(user)

            return jsonify(status="Success", data=True)
        elif self.is_user_logged_in() and Helper.is_user_auth_for_post_review(DatabaseHandler.get_instance().get_user(self.request_data["login"]["email"])):
            title = self.request_data["announcement_data"]["title"]
            info = self.request_data["announcement_data"]["info"]
            content_html = self.request_data["announcement_data"]["content_html"]
            teacher = self.request_data["announcement_data"]["teacher"]
            id = self.request_data["announcement_data"]["id"]

            user = self.database.get_user(self.request_data["login"]["email"])

            announcement = Announcement(title, info, content_html, user.uid, id)

            send_email(receivers=teacher, subject="APHEL TECH ANNOUNCEMENT REVIEW",
                       body="url: {server_ip}/review_confirmed?id={id} <br><br> ***announcement content*** <br> {announcement_content} <br> ***announcement content***"
                       .format(server_ip=Server.ip, announcement_content=announcement.content_html,
                                id=str(AnnouncementReviewHandler.get_instance().new_announcement_review(teacher, announcement).id)))

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

    def validate_review(self):
        review_id = self.request_data["review_id"]
        logging.info("Validation announcement review...")
        return jsonify(data=AnnouncementReviewHandler.get_instance().validate_review(review_id))

    def get_teachers(self):
        teachers = []
        for user in DatabaseHandler.get_instance().get_users():
            if Helper.is_user_admin(user):
                teachers.append(user.uid)
        return jsonify(data=teachers)

    def get_teacher_students(self):
        teacher = DatabaseHandler.get_instance().get_user(self.request_data["email"])
        return jsonify(data=teacher.__dict__["students"])

    def get_user_permission_level(self):
        return jsonify(data=DatabaseHandler.get_instance().get_user(self.request_data["email"]).permission_level)

    def change_user_permission_level(self):
        user = DatabaseHandler.get_instance().get_user(self.request_data["email"])
        permission_level = self.request_data["permission_level"]
        login = self.request_data["login"]

        if self.is_user_logged_in() and Helper.is_user_admin(DatabaseHandler.get_instance().get_user(login["email"])):
            user.permission_level = int(permission_level)
            DatabaseHandler.get_instance().store_user(user)
            return jsonify(data=True, status="Success")

        return jsonify(data=False, status="Failed to change user permission level. User attempting to change "
                                          "permission may not have sufficient privileges.")

    # email or name?@!?!?!??!?!?!?!?
    def add_student_to_teacher(self):
        student_name = self.request_data["student_name"]
        login = self.request_data["login"]
        teacher = DatabaseHandler.get_instance().get_user(login["email"])
        # email or name?@!?!?!??!?!?!?!?
        if self.is_user_logged_in() and Helper.is_user_admin(teacher) and student_name not in teacher.students:
            teacher.students.append(student_name)
            DatabaseHandler.get_instance().store_user(teacher)
            return jsonify(data=True)

        return jsonify(data=False)

    # email or name?@!?!?!??!?!?!?!?
    def remove_student_from_teacher(self):
        student_name = self.request_data["student_name"]
        login = self.request_data["login"]
        teacher = DatabaseHandler.get_instance().get_user(login["email"])

        # email or name?@!?!?!??!?!?!?!?# email or name?@!?!?!??!?!?!?!?# email or name?@!?!?!??!?!?!?!?# email or name?@!?!?!??!?!?!?!?# email or name?@!?!?!??!?!?!?!?
        if self.is_user_logged_in() and Helper.is_user_admin(teacher) and student_name in teacher.students:
            teacher.students.remove(student_name)
            DatabaseHandler.get_instance().store_user(teacher)
            return jsonify(data=True)
        return jsonify(data=False)

    def get_students(self):
        users = DatabaseHandler.get_instance().get_users()
        students = []
        for user in users:
            if not Helper.is_user_admin(user):
                students.append(user.uid)

        return jsonify(data=students)


    def is_user_logged_in(self):
        return self.database.get_user(self.request_data["login"]["email"]).confirmed and \
                   Helper.check_password(self.database.get_user(self.request_data["login"]["email"]).password,
                                     self.request_data["login"]["password"])\

    def is_user_admin(self):
        return jsonify(data=Helper.is_user_admin(DatabaseHandler.get_instance().get_user(self.request_data["email"])))

    def is_user_auth_for_post(self):
        return jsonify(data=Helper.is_user_auth_for_post(DatabaseHandler.get_instance().get_user(self.request_data["email"])))

    def is_user_auth_for_post_review(self):
        return jsonify(data=Helper.is_user_auth_for_post_review(DatabaseHandler.get_instance().get_user(self.request_data["email"])))


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

    @staticmethod
    def is_teacher_email(email):
        # All peel teacher emails are prefixed with "p0"
        return "p0" in email
