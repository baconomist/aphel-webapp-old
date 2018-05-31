import json
import unittest

import os

from main import app
import hashlib

from modules.database_handler import DatabaseHandler
from modules.user import User

DatabaseHandler._databaseLocation = os.path.join(os.path.dirname(__file__), "..", "data", "test_database.json")

class MainTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get(self):
        response = self.app.get('/')

    def test_login(self):
        response =json.loads(self.login("test_user@pdsb.net", self.encrypt_string("test_password")).get_data(as_text=True))
        assert response["data"]


    def test_signup(self):
        # b in front of string to turn it into a bytes object
        response = json.loads(self.signup("test_user@pdsb.net", self.encrypt_string("test_password")).get_data(as_text=True))
        assert response["data"] and not DatabaseHandler.get_instance().user_exists("test_user@pdsb.net")
        assert not response["data"] and DatabaseHandler.get_instance().user_exists("test_user@pdsb.net")

    def test_database(self):
        database = DatabaseHandler.get_instance()
        database.store_user(User("test_user@pdsb.net", self.encrypt_string("test_password")))
        assert database.get_user("test_user@pdsb.net") is not None, b"Couldn't retrieve user from database!"

        user_names = []
        for user in database.get_users():
            user_names.append(user.uid)
        assert "test_user" in user_names, b"Retrieving all users does not work!"

    def encrypt_string(self, hash_string):
        sha_signature = \
            hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature

    def signup(self, username, password):
        return self.app.post('/', data=json.dumps(dict(
            function="signup",
            data=dict(login=dict(email=username, password=password))
        )), content_type='application/json', follow_redirects=True)

    def login(self, username, password):
        return self.app.post('/', data=json.dumps(dict(
            function="login",
            data=dict(login=dict(email=username, password=password))
        )), content_type='application/json', follow_redirects=True)


if __name__ == '__main__':
    unittest.main()