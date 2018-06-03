import os
from bs4 import BeautifulSoup
from flask import Markup


class HTML_Module(object):
    def __init__(self, raw_html):

        self.bs4Obj: BeautifulSoup = None
        self.children: list = []

        self.parse_html(raw_html)

    def parse_html(self, raw_html):
        parsed_html = BeautifulSoup(raw_html, "html.parser")

        self.bs4Obj = parsed_html.find()

        if self.bs4Obj is not None:
            children = self.bs4Obj.find_all(recursive=False)

            if len(children) > 0:
                for child in children:
                    self.children.append(HTML_Module(str(child)))

    def get_raw_html(self):
        return str(self.bs4Obj)

    def get_markup(self):
        return Markup(str(self.bs4Obj))
