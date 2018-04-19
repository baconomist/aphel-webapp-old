import time
import hashlib
import random


class Confirmation(object):
    def __init__(self):
        self.id = self.generate_new_url_hash().hexdigest()
        self.time_created = time.time()

        twenty_four_hours_in_millis = (24*60*60*1000)
        self.time_before_expired = time.time() + twenty_four_hours_in_millis

    def generate_new_url_hash(self):
        return hashlib.md5(str(time.time() + random.randint(0, 9999)).encode())

    def is_valid(self):
        return time.time() < self.time_before_expired
