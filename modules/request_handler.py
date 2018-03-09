from modules.database_handler import DatabaseHandler
from modules.user import User

class RequestHandler(object):

    def login(self, request):
        assert request.method == "POST", b'The request method for login() was not "POST"!'


    def sign_up(self, request):
        assert request.method == "POST", b'The request method for sign_up() was not "POST"!'
        database = DatabaseHandler.get_instance()
        data = request.form.getlist("login[]")
        database.store_user(User(data[0], data[1]))

    def is_user_admin(self, request):
        database = DatabaseHandler.get_instance()
        return database.get_user(request.form.get("user")).get_permission_level() > 1

    def is_user_auth_for_post(self, request):
        database = DatabaseHandler.get_instance()
        return database.get_user(request.form.get("user")).get_permission_level() > 0
