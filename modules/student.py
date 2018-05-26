from modules.user import User
import json

class Student(User):
    def __init__(self, uid, password):
        super(Student, self).__init__(uid, password)
        self.grade = 9
        self.permission_level = self.get_new_student_permission_level()

    def get_profile_info_json(self):
        profile_data = json.loads(super(Student, self).get_profile_info_json())
        profile_data["grade"] = self.grade
        return json.dumps(profile_data)