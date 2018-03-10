import unittest
from main import app
import hashlib

from modules.database_handler import DatabaseHandler
from modules.user import User

class MainTest(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get(self):
        response = self.app.get('/')

    def test_login(self):
        pass

    def test_signup(self):
        # b in front of string to turn it into a bytes object
        response = self.sign_up("test_user", self.encrypt_string("test_password"))
        assert response.data == b'Success'

    def test_database(self):
        database = DatabaseHandler.get_instance()
        database.store_user(User("test_user", "test_password"))
        assert database.get_user("test_user") is not None, b"Couldn't retrieve user from database!"

        user_names = []
        for user in database.get_users():
            user_names.append(user.name)
        assert "test_user" in user_names, b"Retrieving all users does not work!"

    def encrypt_string(self, hash_string):
        sha_signature = \
            hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature

    def sign_up(self, username, password):

        return self.app.post('/signup', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)


if __name__ == '__main__':
    unittest.main()