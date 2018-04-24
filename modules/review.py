import hashlib
import time
import random

from modules.user import User

class Review(object):
    def __init__(self, teacher: User, student: User, announcement):
        self.teacher = teacher
        self.student = student
        self.announcement = announcement
        self.id = self.generate_new_url_hash().hexdigest()

    def generate_new_url_hash(self):
        return hashlib.md5(str(time.time() + random.randint(0, 9999)).encode())
