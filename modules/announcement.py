import datetime
import json

class Announcement(object):
    def __init__(self, content_html: str, user_name: str, id: int):
        self.content_html = content_html
        self.user_name = user_name
        self.date_created = datetime.datetime.now()
        self.id = id

    def to_json(self):
        # can't serialize self.date_created
        return json.dumps({"content_html": self.content_html, "user_name": self.user_name, "id": self.id})
