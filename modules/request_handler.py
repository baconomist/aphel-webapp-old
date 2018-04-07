from modules.database_handler import DatabaseHandler
from modules.user import User
import logging
import hashlib, uuid
from flask import jsonify, request


class RequestHandler(object):
    def __init__(self):
        # This is why this class needs an instance,
        # The app crashes if this dict is static
        self.functions = {"user_exists": DatabaseHandler.get_instance().user_exists}

    def handle_abstract(self):
        try:
            return jsonify(data=self.functions[request.form.get("function")](request.form.get("data")),
                           status="Success")
        except:
            return jsonify(data="Failed to execute abstract request!", status="Error",
                           reason="No matching function found: {function}".format(function=request.form.get("function")))

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
        user = User(data["email"], data["password"])
        if "Success" in self.is_user_valid(user):
            database.store_user(User(data.get("email"), self.hash_password(data.get("password"))))
        return self.is_user_valid(user)

    def do_login(self, data):
        for user in DatabaseHandler.get_instance().get_users():
            if user.name == data.get("email") and self.check_password(user.password, data.get("password")):
                return "Logged in as %s" % user.name

        return "Failed to log in. The login credentials may be incorrect " \
               "\n or the user does not exist."

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

    def is_user_valid(self, user):
        database = DatabaseHandler.get_instance()
        if not database.user_exists(user.name) and len(user.password) >= 8 and "@pdsb.net" in user.name:
            return "Successfully signed up %s" % user.name
        elif len(user.password) < 8:
            return "Failed to sign up! Password has to be >= 8  characters in length"
        elif not "@pdsb.net" in user.name:
            return "Failed to signup! You must use your @pdsb.net email!"
        else:
            return "Failed to sign up! User %s already exists!" % user.name

    def hash_password(self, password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    def check_password(self, hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
