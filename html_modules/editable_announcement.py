import os

from html_modules.html_module import HTML_Module


class EditableAnnouncement(HTML_Module):
    def __init__(self):
        file = open(os.path.join(os.path.dirname(__file__), "editable_announcement.html"), "r")
        file_data = file.read()
        file.close()

        super(EditableAnnouncement, self).__init__(file_data)

