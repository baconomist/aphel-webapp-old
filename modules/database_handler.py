import json, jsonpickle
from modules.user import User
import logging

class DatabaseHandler(object):

    databaseLocation = "../data/database.json"

    def __init__(self):
        try:
            self.load_data()
        except:
            self.raw_data = {"users": []}

    def load_data(self):
        logging.info("Loading database...")

        file = open(DatabaseHandler.databaseLocation, "r+")
        self.raw_data = json.load(file)

        logging.info("Database Loaded.")

    def store_user(self, user):
        logging.info("Storing user:" + str(user.name))

        user = jsonpickle.encode(user)
        if user not in self.raw_data["users"]:
            self.raw_data["users"].append(user)
        self.write()

    def remove_user(self, username=""):

        logging.info("Removing user:" + username)

        raw_data = self.raw_data.copy()

        count = 0
        for u in raw_data["users"]:
            if jsonpickle.decode(u).name == username:
                self.raw_data["users"].pop(count)
                self.write()
                break
            count += 1

    def write(self):
        logging.info("Writing to database.")

        file = open(DatabaseHandler.databaseLocation, "w")
        json.dump(self.raw_data, file, sort_keys=True, indent=4)

    def get_users(self):
        data = self.raw_data
        count = 0
        for user in self.raw_data["users"]:
            data["users"][count] = jsonpickle.decode(user)
            count += 1
        return data

databaseHandler = DatabaseHandler()


