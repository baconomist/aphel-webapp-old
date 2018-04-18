import time
import hashlib
import random


class Confirmation(object):
    def __init__(self):
        self.id = self.generate_new_url_hash().hexdigest()
        self.time_created = time.time()
        self.time_before_expired = time.time() + (24 * 60 * 60 * 1000)

    def generate_new_url_hash(self):
        return hashlib.md5(str(time.time() + random.randint(0, 9999)).encode())
