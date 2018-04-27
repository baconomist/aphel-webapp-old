from modules.user import User
import json

class Teacher(User):
    def __init__(self, uid, password):
        super(Teacher, self).__init__(uid, password)
        self.students = []
        self.permission_level = self.get_teacher_permisison_level()




