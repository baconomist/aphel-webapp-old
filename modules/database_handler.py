import json, jsonpickle
from modules.user import User
import logging
import copy
import os
import datetime


class DatabaseHandler(object):
    _databaseLocation = os.path.join(__file__, "..\\..\\data\\database.json")

    _instance = None

    def __init__(self):
        try:
            self.load_data()
        except:
            self.raw_data = {"users": []}

    def load_data(self):
        logging.info("Loading database...")

        file = open(DatabaseHandler._databaseLocation, "r+")
        self.raw_data = json.load(file)
        file.close()

        logging.info("Database Loaded.")

    def store_user(self, user):
        logging.info("Storing user: " + user.uid)

        if self.get_user(user.uid) != None:
            count = 0
            for u in self.raw_data["users"]:
                if jsonpickle.decode(u).uid == user.uid:
                    self.raw_data["users"][count] = jsonpickle.encode(user)
                count += 1
        else:
            self.raw_data["users"].append(jsonpickle.encode(user))

        self.write()

    def remove_user(self, username):

        logging.info("Removing user: " + username)

        raw_data = self.raw_data.copy()

        count = 0
        for u in raw_data["users"]:
            if jsonpickle.decode(u).name == username:
                self.raw_data["users"].pop(count)
                self.write()
                break
            count += 1

    def get_user(self, username):

        logging.info("Getting user: " + username)

        for user in self.get_users():
            if user.uid == username:
                logging.info("User found: " + username)
                return user

        logging.info("User not found: " + username)

    def user_exists(self, username: str):
        for user in self.get_users():
            if user.uid == username:
                return True
        return False

    def write(self):
        logging.info("Writing to database.")

        file = open(DatabaseHandler._databaseLocation, "w")
        json.dump(self.raw_data, file, sort_keys=True, indent=4)
        file.close()

    def get_users(self):
        data = copy.deepcopy(self.raw_data)
        count = 0
        for user in self.raw_data["users"]:
            data["users"][count] = jsonpickle.decode(user)
            count += 1
        return data["users"]

    def get_announcements_json(self):
        announcement_dates = {}

        for user in self.get_users():
            for announcement in user.announcements:
                announcement_dates[announcement.time_stamp] = announcement

        announcements = []
        for announcement_date in sorted(announcement_dates.keys(), key=int):
            announcements.append(announcement_dates[announcement_date])

        print(announcement_dates)
        announcements_json = []
        for announcement in announcements:
            announcements_json.append(announcement.to_json())

        return announcements_json

    @staticmethod
    def get_instance():
        if DatabaseHandler._instance is None:
            DatabaseHandler._instance = DatabaseHandler()
            return DatabaseHandler._instance
        else:
            return DatabaseHandler._instance
