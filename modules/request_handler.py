import json
import os
from functools import wraps

from modules.database_handler import DatabaseHandler
from modules.confirmation_manager import ConfirmationManager
from modules.announcement_review_handler import AnnouncementReviewHandler
from modules.profanity_filter import ProfanityFilter

from modules.student import Student
from modules.teacher import Teacher

from modules.announcement import Announcement

import config

from modules.emailer import send_email

import traceback

import logging
import hashlib, uuid
from flask import jsonify, request, session

''' ATTENTION '''
''' ALL METHODS IN REQUEST HANDLER ARE CALLABLE BY CLIENT '''
''' MAKE SURE THE METHODS HERE ARE SECURE '''
''' ATTENTION '''


# https://stackoverflow.com/questions/308999/what-does-functools-wraps-do

def login_required(request_function):
    @wraps(request_function)
    def wrapper(*args, **kwargs):
        database = DatabaseHandler.get_instance()

        # Continue running the function, otherwise return an error
        return request_function(*args, **kwargs) if session.get("uid") is not None and database.get_user(
            session.get("uid")).confirmed \
            else jsonify(data=False, status="Failed to log in.")

    return wrapper


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

        for user in self.database.get_users():
            if user.confirmed and user.uid == email and Helper.check_password(user.password, password):
                logging.info("Logged in as %s" % user.uid)
                session["uid"] = user.uid
                return jsonify(data=True, status="Logged in as %s" % user.uid)

        logging.info("Failed to log in. The login credentials may be incorrect "
                     "\n or the user does not exist.")
        return jsonify(data=False,
                       status="Failed to log in. The login credentials may be incorrect, the user might not be "
                              "confirmed "
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
                user = Student(email, Helper.hash_password(password))

            id = str(ConfirmationManager.get_instance().new_confirmation(user).id)

            send_email(receivers=email, subject="APHEL TECH EMAIL CONFIRMATION",
                       body=r"url: http://{server_ip}/confirmation_confirmed?id={id}".format(
                           server_ip=config.public_address, id=id))

            self.database.store_user(user)

            logging.info(is_user_valid)

            return jsonify(data=True, status=is_user_valid)

        logging.info(is_user_valid)

        return jsonify(data=False, status=is_user_valid)

    def get_dashboard(self):
        return jsonify(data=self.database.get_announcements_json())

    @login_required
    def save_announcement(self):

        user = self.database.get_user(session.get("uid"))

        if Helper.is_user_auth_for_post(user):

            title = self.request_data["announcement_data"]["title"]
            info = self.request_data["announcement_data"]["info"]
            content_html = self.request_data["announcement_data"]["content_html"]
            id = self.request_data["announcement_data"]["id"]
            user = self.database.get_user(session.get("uid"))
            print(title, info, content_html, id, user)
            swearing_filter = ProfanityFilter()
            if not swearing_filter.is_profane(content_html):
                user.create_announcement(title=title, info=info, content_html=content_html, id=int(id))
            else:
                print("User entered a profane message")
                # DO NOT USE PROFANE LANGUAGE alert shows up

            self.database.store_user(user)

            return jsonify(status="Success", data=True)
        elif Helper.is_user_auth_for_post_review(user):

            title = self.request_data["announcement_data"]["title"]
            info = self.request_data["announcement_data"]["info"]
            content_html = self.request_data["announcement_data"]["content_html"]
            teacher = self.request_data["announcement_data"]["teacher"]
            id = self.request_data["announcement_data"]["id"]

            announcement = Announcement(title, info, content_html, user.uid, id)

            send_email(receivers=teacher, subject="APHEL TECH ANNOUNCEMENT REVIEW",
                       body="url: http://{server_ip}/review_confirmed?id={id} <br><br> ***announcement content*** <br> {announcement_content} <br> ***announcement content***"
                       .format(server_ip=config.public_address, announcement_content=announcement.content_html,
                               id=str(AnnouncementReviewHandler.get_instance().new_announcement_review(teacher,
                                                                                                       announcement).id)))

            self.database.store_user(user)

            return jsonify(status="Success", data=True)
        else:
            return jsonify(status="Error", data=False)

    def user_exists(self):
        return jsonify(data=self.database.user_exists(self.request_data))

    @login_required
    def delete_announcement(self):
        email = session.get("uid")
        announcement_id = self.request_data["announcement_id"]

        user = self.database.get_user(email)
        user.remove_announcement_by_id(int(announcement_id))
        self.database.store_user(user)
        return "Announcement deleted"

    def validate_confirmation(self):
        confirmation_id = self.request_data["confirmation_id"]
        logging.info("Validating confirmation link...")
        return jsonify(data=ConfirmationManager.get_instance().validate_confirmation(confirmation_id))

    def validate_review(self):
        review_id = self.request_data["review_id"]
        logging.info("Validation announcement review...")
        return jsonify(data=AnnouncementReviewHandler.get_instance().validate_review(review_id))

    @login_required
    def get_teacher_students(self):
        teacher = DatabaseHandler.get_instance().get_user(self.request_data["email"])
        print(teacher.__dict__["students"])
        return jsonify(data=teacher.__dict__["students"])

    def get_user_permission_level(self):
        return jsonify(data=DatabaseHandler.get_instance().get_user(self.request_data["email"]).permission_level)

    @login_required
    def change_user_permission_level(self):
        user = DatabaseHandler.get_instance().get_user(self.request_data["email"])
        permission_level = self.request_data["permission_level"]
        login = self.request_data["login"]

        if Helper.is_user_admin(DatabaseHandler.get_instance().get_user(login["email"])):
            user.permission_level = int(permission_level)
            DatabaseHandler.get_instance().store_user(user)
            return jsonify(data=True, status="Success")

        return jsonify(data=False, status="Failed to change user permission level. User attempting to change "
                                          "permission may not have sufficient privileges.")

    # email or name?@!?!?!??!?!?!?!?
    @login_required
    def add_student_to_teacher(self):
        student_name = self.request_data["student_name"]
        login = self.request_data["login"]
        teacher = DatabaseHandler.get_instance().get_user(login["email"])
        # email or name?@!?!?!??!?!?!?!?
        if Helper.is_user_admin(teacher) and student_name not in teacher.students:
            teacher.students.append(student_name)
            DatabaseHandler.get_instance().store_user(teacher)
            return jsonify(data=True)

        return jsonify(data=False)

    # email or name?@!?!?!??!?!?!?!?
    @login_required
    def remove_student_from_teacher(self):
        student_name = self.request_data["student_name"]
        login = self.request_data["login"]
        teacher = DatabaseHandler.get_instance().get_user(login["email"])

        # email or name?@!?!?!??!?!?!?!?# email or name?@!?!?!??!?!?!?!?# email or name?@!?!?!??!?!?!?!?# email or name?@!?!?!??!?!?!?!?# email or name?@!?!?!??!?!?!?!?
        if Helper.is_user_admin(teacher) and student_name in teacher.students:
            student = DatabaseHandler.get_instance().get_user(student_name)
            student.permission_level = 0
            DatabaseHandler.get_instance().store_user(student)

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

    @login_required
    def save_profile_data(self):
        firstname = self.request_data["firstname"]
        lastname = self.request_data["lastname"]

        grade = self.request_data["grade"]

        user = self.database.get_user(self.request_data["login"]["email"])

        if grade != None:
            user: Student

            user.firstname = firstname
            user.lastname = lastname
            user.grade = grade
        else:
            user: Teacher

            user.firstname = firstname
            user.lastname = lastname

        self.database.store_user(user)

        return jsonify(data=True)

    @login_required
    def handle_file_upload(self):
        email = self.request_data["login"]["email"]

        file = open(os.path.join(os.path.dirname(__file__),
                                 "..", "data", "profile_images", email + ".jpg"), "wb")
        file.write(request.get_data())
        file.close()
        return jsonify(data=True)

    def get_profile_data(self):
        email = self.request_data["email"]

        profile_dat = json.loads(self.database.get_user(email).get_profile_info_json())
        # profile_dat["profile_image"] = open(os.path.join(__file__, "..\\..\\data\\profile_images\\"+email+".jpg"), "rb").read()
        # profile_dat
        profile_dat = json.dumps(profile_dat)
        return jsonify(data=profile_dat)

    def is_user_admin(self):
        return jsonify(data=Helper.is_user_admin(DatabaseHandler.get_instance().get_user(self.request_data["email"])))

    def is_user_auth_for_post(self):
        return jsonify(
            data=Helper.is_user_auth_for_post(DatabaseHandler.get_instance().get_user(self.request_data["email"])))

    def is_user_auth_for_post_review(self):
        return jsonify(data=Helper.is_user_auth_for_post_review(
            DatabaseHandler.get_instance().get_user(self.request_data["email"])))


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
        return user.get_permission_level() >= user.get_teacher_permisison_level()

    @staticmethod
    def is_user_auth_for_post(user):
        return user.get_permission_level() > user.get_trusted_student_permission_level()

    @staticmethod
    def is_user_auth_for_post_review(user):
        return user.get_permission_level() > user.get_untrusted_student_permission_level()

    @staticmethod
    def is_teacher_email(email):
        # All peel teacher emails are prefixed with "p0"
        return "p0" in email
