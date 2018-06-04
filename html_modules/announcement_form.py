import os

from cssutils import parseStyle
from jinja2 import Template

from html_modules.html_module import HTML_Module


class AnnouncementForm(HTML_Module):
    def __init__(self, trusted_post, announcement_id, teacher_uid_list):

        file = open(os.path.join(os.path.dirname(__file__), "announcement_form.html"), "r")
        file_data = file.read()
        file.close()

        file_data = Template(file_data).render(announcement_id=announcement_id, teacher_uids=teacher_uid_list)

        super(AnnouncementForm, self).__init__(file_data)

        if trusted_post:
            style = self.bs4Obj.find(class_="ann-post")["style"]
            self.bs4Obj.find(class_="ann-post")["style"] = parseStyle(style).removeProperty("display")

            # Remove the other announcement template
            self.bs4Obj.find(class_="ann-post-review").decompose()

        else:
            style = self.bs4Obj.find(class_="ann-post-review")["style"]
            self.bs4Obj.find(class_="ann-post-review")["style"] = parseStyle(style).removeProperty("display")

            # Remove the other announcement template
            self.bs4Obj.find(class_="ann-post").decompose()
