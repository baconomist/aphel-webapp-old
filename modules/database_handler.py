import json, jsonpickle
from modules import user
from collections import namedtuple


class DatabaseHandler(object):
    def __init__(self):
        try:
            self.load_data()
        except:
            self.data = {"users": []}

        self.store_user(user.User("bib", "123"))

    def load_data(self):
        file = open("../data/database.json", "r+")
        self.data = json.load(file)

    def store_user(self, user):
        user = jsonpickle.encode(user)
        print(user)
        if user not in self.data["users"]:
            self.data["users"].append(user)
        self.write()

    def write(self):
        file = open("../data/database.json", "w")
        json.dump(self.data, file, sort_keys=True, indent=4)

    def get_users(self):
        data = self.data
        count = 0
        for user in self.data["users"]:
            data["users"][count] = jsonpickle.decode(user)
            count += 1
        return data


databaseHandler = DatabaseHandler()

print(databaseHandler.get_users())

#x = json.load(databaseHandler.file, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

