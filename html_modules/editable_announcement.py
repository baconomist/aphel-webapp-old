import os

from html_modules.html_module import HTML_Module
from jinja2 import Template

from modules.announcement import Announcement


class EditableAnnouncement(HTML_Module):
    def __init__(self, announcement: Announcement):
        file = open(os.path.join(os.path.dirname(__file__), "editable_announcement.html"), "r")
        file_data = file.read()
        file.close()

        file_data = Template(file_data).render(announcement_id=announcement.id, announcement_title=announcement.title,
                                               announcement_info=announcement.info,
                                               announcement_content=announcement.content_html,
                                               announcement_timestamp=announcement.time_stamp)

        super(EditableAnnouncement, self).__init__(file_data)

