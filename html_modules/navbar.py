import os

from flask import Markup

navbar_markup = Markup(open(os.path.join(os.path.dirname(__file__), "navbar.html"), "r").read())
