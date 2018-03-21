from modules.database_handler import DatabaseHandler
from modules.user import User
import logging
import hashlib, uuid

class RequestHandler(object):
    def login(self, request):
        logging.info("Logging in...")
        assert request.method == "POST", b'The request method for login() was not "POST"!'
        data = request.form
        result = self.do_login(data)
        logging.info(result)
        return result


    def do_login(self, data):
        for user in DatabaseHandler.get_instance().get_users():
            if user.name == data.get("email") and self.check_password(self.hash_password(data.get("password")), data.get("password")):
                return "Logged in as %s" % user.name

        return "Failed to log in. User may not have signed up."

    def signup(self, request):
        assert request.method == "POST", b'The request method for signup() was not "POST"!'
        database = DatabaseHandler.get_instance()
        data = request.form
        print(self.hash_password(data.get("password")))
        database.store_user(User(data.get("email"), self.hash_password(data.get("password"))))
        return "Success"

    def is_user_admin(self, request):
        database = DatabaseHandler.get_instance()
        data = request.form
        return database.get_user(data.get("email")).get_permission_level() > 2

    def is_user_auth_for_post(self, request):
        database = DatabaseHandler.get_instance()
        data = request.form
        return database.get_user(data.get("email")).get_permission_level() > 1

    def is_user_auth_for_post_review(self, request):
        database = DatabaseHandler.get_instance()
        data = request.form
        return database.get_user(data.get("email")).get_permission_level() > 0

    def hash_password(self, password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    def check_password(self, hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
