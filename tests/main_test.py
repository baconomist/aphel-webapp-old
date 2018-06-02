import json
import unittest

import os

# Before importing "main.py", need to set Database location
# DatabaseHandler.get_instance used in request handler on init
# Request handler instance is created on import of "main.py"
from modules.database_handler import DatabaseHandler

DatabaseHandler._databaseLocation = os.path.join(os.path.dirname(__file__), "..", "data", "test_database.json")

from main import app
from modules.user import User
from modules import request_handler


def clear_database():
    DatabaseHandler.get_instance().raw_data = {}
    DatabaseHandler.get_instance().write()


def signup(app_instance, username, password):
    return app_instance.post('/', data=json.dumps(dict(
        function="signup",
        data=dict(login=dict(email=username, password=password))
    )), content_type='application/json', follow_redirects=True)


def login(app_instance, username, password):
    return app_instance.post('/', data=json.dumps(dict(
        function="login",
        data=dict(login=dict(email=username, password=password))
    )), content_type='application/json', follow_redirects=True)


class MainTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

        self.test_uid = "test_user@pdsb.net"
        self.test_password = "test_password"

    def test_get(self):
        response = self.app.get('/')

    def test_login(self):
        user = DatabaseHandler.get_instance().get_user(self.test_uid)
        user.confirmed = True
        DatabaseHandler.get_instance().store_user(user)

        response = json.loads(login(self.app, self.test_uid, self.test_password).get_data(as_text=True))
        assert response["data"]

    def test_signup(self):
        # b in front of string to turn it into a bytes object
        response = json.loads(signup(self.app, self.test_uid, self.test_password).get_data(as_text=True))
        assert (response["data"] and not DatabaseHandler.get_instance().user_exists(self.test_uid)) \
        or (not response["data"] and DatabaseHandler.get_instance().user_exists(self.test_uid))

    def test_database(self):
        database = DatabaseHandler.get_instance()
        database.store_user(User(self.test_uid, request_handler.Helper.hash_password(self.test_password)))
        assert database.get_user(self.test_uid) is not None, b"Couldn't retrieve user from database!"

        user_names = []
        for user in database.get_users():
            user_names.append(user.uid)
        assert self.test_uid in user_names, b"Retrieving all users does not work!"


if __name__ == '__main__':
    unittest.main()
