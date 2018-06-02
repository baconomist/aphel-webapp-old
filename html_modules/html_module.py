import os
from bs4 import BeautifulSoup
from flask import Markup


class HTML_Module(object):

    def __init__(self, raw_html):

        self.raw_html = raw_html
        self.markup = Markup(self.raw_html)

        self.bs4Obj = None
        self.children = []

        self.parse_html()

    def parse_html(self):
        parsed_html = BeautifulSoup(self.raw_html, "html.parser")

        self.bs4Obj = parsed_html.find()

        if self.bs4Obj != None:
            children = self.bs4Obj.find_all(recursive=False)

            if len(children) > 0:
                for child in children:
                    self.children.append(HTML_Module(str(child)))



