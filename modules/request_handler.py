from modules.database_handler import DatabaseHandler
from modules.user import User
import logging
import hashlib, uuid

class RequestHandler(object):
    
    @staticmethod
    def login(request):
        logging.info("RequestHandler: Logging in...")
        assert request.method == "POST", b'The request method for login() was not "POST"!'
        data = request.form
        result = RequestHandler.do_login(data)
        logging.info(result)
        return result

    @staticmethod
    def signup(request):
        logging.info("RequestHandler: Signing up...")
        assert request.method == "POST", b'The request method for signup() was not "POST"!'
        data = request.form
        result = RequestHandler.do_signup(data)
        logging.info(result)
        return result

    @staticmethod
    def do_signup(data):
        database = DatabaseHandler.get_instance()
        if database.get_user(data.get("email")) == None and data.get("password").length > 6:
            database.store_user(User(data.get("email"), RequestHandler.hash_password(data.get("password"))))
            return "Successfully signed up %s" % data.get("email")
        elif data.get("password").length < 6:
            return "Failed to sign up! Password has to be > 6 characters in length"
        return "Failed to sign up! User %s already exists!" % data.get("email")

    @staticmethod
    def do_login(data):
        for user in DatabaseHandler.get_instance().get_users():
            if user.name == data.get("email") and RequestHandler.check_password(user.password, data.get("password")):
                return "Logged in as %s" % user.name

        return "Failed to log in. The login credentials may be incorrect " \
               "\n or the user does not exist."

    @staticmethod
    def is_user_admin(request):
        database = DatabaseHandler.get_instance()
        data = request.form
        return database.get_user(data.get("email")).get_permission_level() > 2

    @staticmethod
    def is_user_auth_for_post(request):
        database = DatabaseHandler.get_instance()
        data = request.form
        return database.get_user(data.get("email")).get_permission_level() > 1

    @staticmethod
    def is_user_auth_for_post_review(request):
        database = DatabaseHandler.get_instance()
        data = request.form
        return database.get_user(data.get("email")).get_permission_level() > 0

    @staticmethod
    def hash_password(password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    @staticmethod
    def check_password(hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
