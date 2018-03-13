from modules.database_handler import DatabaseHandler
from modules.user import User
import logging

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
            if user.name == data.get("username") and user.password == data.get("password"):
                return "Logged in as %s" % user.name

        return "Failed to log in."

    def signup(self, request):
        assert request.method == "POST", b'The request method for signup() was not "POST"!'
        database = DatabaseHandler.get_instance()
        data = request.form
        database.store_user(User(data.get("username"), data.get("password")))
        return "Success"

    def is_user_admin(self, request):
        database = DatabaseHandler.get_instance()
        data = request.form
        return database.get_user(data.get("username")).get_permission_level() > 2

    def is_user_auth_for_post(self, request):
        database = DatabaseHandler.get_instance()
        data = request.form
        return database.get_user(data.get("username")).get_permission_level() > 1

    def is_user_auth_for_post_review(self, request):
        database = DatabaseHandler.get_instance()
        data = request.form
        return database.get_user(data.get("username")).get_permission_level() > 0
