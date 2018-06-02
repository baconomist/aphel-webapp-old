import os

from flask import Markup
from html_modules.html_module import HTML_Module

class Navbar(HTML_Module):
    def __init__(self):
        file = open(os.path.join(os.path.dirname(__file__), "navbar.html"), "r")
        file_data = file.read()
        file.close()

        super(Navbar, self).__init__(file_data)

