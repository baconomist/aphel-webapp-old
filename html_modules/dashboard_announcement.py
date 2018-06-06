import os

from jinja2 import Template

from html_modules.html_module import HTML_Module


class DashboardAnnouncement(HTML_Module):
    def __init__(self, uid, title, info, content, time_stamp):
        file = open(os.path.join(os.path.dirname(__file__), "dashboard_announcement.html"), "r")
        file_data = file.read()
        file.close()

        file_data = Template(file_data).render(uid=uid, title=title, info=info,
                             content=content, time_stamp=time_stamp)

        super(DashboardAnnouncement, self).__init__(file_data)

