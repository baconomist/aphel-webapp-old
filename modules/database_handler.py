import json, jsonpickle
from modules.user import User
import logging
import copy


class DatabaseHandler(object):
    databaseLocation = "./data/database.json"

    _instance = None

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
        logging.info("Storing user:" + user.name)

        if self.get_user(user.name) != None:
            count = 0
            print(self.raw_data)
            for u in self.raw_data["users"]:
                if jsonpickle.decode(u).name == user.name:
                    self.raw_data["users"][count] = jsonpickle.encode(user)
                count += 1
        else:
            self.raw_data["users"].append(jsonpickle.encode(user))

        self.write()

    def remove_user(self, username):

        logging.info("Removing user:" + username)

        raw_data = self.raw_data.copy()

        count = 0
        for u in raw_data["users"]:
            if jsonpickle.decode(u).name == username:
                self.raw_data["users"].pop(count)
                self.write()
                break
            count += 1

    def get_user(self, username):

        logging.info("Getting user:" + username)

        for user in self.get_users():
            if user.name == username:
                logging.info("User found:" + username)
                return user

        logging.info("User not found:" + username)

    def write(self):
        logging.info("Writing to database.")

        file = open(DatabaseHandler.databaseLocation, "w")
        json.dump(self.raw_data, file, sort_keys=True, indent=4)

    def get_users(self):
        data = copy.deepcopy(self.raw_data)
        count = 0
        for user in self.raw_data["users"]:
            data["users"][count] = jsonpickle.decode(user)
            count += 1
        return data["users"]

    @staticmethod
    def get_instance():
        if DatabaseHandler._instance is None:
            DatabaseHandler._instance = DatabaseHandler()
            return DatabaseHandler._instance
        else:
            return DatabaseHandler._instance

