import os

from jinja2 import Template

from html_modules.html_module import HTML_Module


class DashboardAnnouncement(HTML_Module):
    def __init__(self, announcement):
        file = open(os.path.join(os.path.dirname(__file__), "dashboard_announcement.html"), "r")
        file_data = file.read()
        file.close()

        file_data = Template(file_data).render(uid=announcement.user_name, title=announcement.title, info=announcement.info,
                             content_raw=announcement.get_content_raw(), time_stamp=announcement.time_stamp)

        super(DashboardAnnouncement, self).__init__(file_data)

