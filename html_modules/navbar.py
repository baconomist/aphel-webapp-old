import os

from flask import Markup

class NavBar(object):
    def __init__(self):
        self.markup = Markup(open(os.path.join(os.path.dirname(__file__), "navbar.html"), "r").read())
