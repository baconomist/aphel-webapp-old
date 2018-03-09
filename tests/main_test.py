import os
import flask
import unittest
import tempfile
from main import app


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get(self):
        response = self.app.get('/')
        print(response)

    def test_login_logout(self):
        # b in front of string to turn it into a bytes objectz
        '''response = self.login('admin', 'default')
        assert b'You were logged in' in response.data
        response = self.logout()
        assert b'You were logged out' in response.data
        response = self.login('adminx', 'default')
        assert b'Invalid username' in response.data
        response = self.login('admin', 'defaultx')
        assert b'Invalid password' in response.data'''

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)


if __name__ == '__main__':
    unittest.main()