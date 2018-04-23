import datetime
import json
import time

class Announcement(object):
    def __init__(self, title: str, info: str, content_html: str, user_name: str, id: int):
        self.title = title
        self.info = info
        self.content_html = content_html
        self.user_name = user_name
        self.time_stamp = time.time()
        self.id = id

    def to_json(self):
        # can't serialize self.date_created
        return json.dumps({"title": self.title, "info": self.info, "content_html": self.content_html, "user_name": self.user_name,
                           "time_stamp": self.time_stamp, "id": self.id})
