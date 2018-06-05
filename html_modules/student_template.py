import os

from jinja2 import Template

from html_modules.html_module import HTML_Module


class StudentTemplate(HTML_Module):
    def __init__(self, student_uid, student_perm, student_name):
        file = open(os.path.join(os.path.dirname(__file__), "student_template.html"), "r")
        file_data = file.read()
        file.close()

        file_data = Template(file_data).render(student_uid=student_uid, student_perm=student_perm,
                                               student_name=student_name,
                                               template_id=student_uid.replace("@pdsb.net", ""))

        super(StudentTemplate, self).__init__(file_data)