import json
import jsonpickle
from modules.user import User
from modules.club import Club
from typing import List
import logging
import copy
import os


class DatabaseHandler(object):
    _databaseLocation = os.path.join(os.path.dirname(__file__), "..", "data", "database.json")

    _instance = None

    def __init__(self):
        try:
            self.load_data()
        except:
            self.raw_data = {"users": [], "clubs": []}

    def load_data(self):

        logging.info("Loading database...")

        file = open(DatabaseHandler._databaseLocation, "r+")
        self.raw_data = json.load(file)
        file.close()

        logging.info("Database Loaded.")

    def store_user(self, user: User):
        logging.info("Storing user: " + user.uid)

        if self.get_user(user.uid) is not None:
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
            if jsonpickle.decode(u).uid == username:
                self.raw_data["users"].pop(count)
                self.write()
                break
            count += 1

        self.write()

    def get_user(self, username):
        logging.info("Getting user: " + username)

        for user in self.get_users():
            if user.uid == username:
                logging.info("User found: " + username)
                return user

        logging.info("User not found: " + username)

    def user_exists(self, username: str) -> bool:
        for user in self.get_users():
            if user.uid == username:
                return True
        return False

    def get_users(self) -> List[User]:
        data = copy.deepcopy(self.raw_data)
        count = 0
        for user in self.raw_data["users"]:
            data["users"][count] = jsonpickle.decode(user)
            count += 1
        return data["users"]

    def get_announcements_json(self):
        announcements_json = []

        for user in self.get_users():
            for announcement in user._announcements:
                announcements_json.append(announcement.to_json())

        return announcements_json

    def store_club(self, club: Club):
        logging.info("Storing club: " + club.name)

        if self.get_user(club.name) is not None:
            count = 0
            for u in self.raw_data["clubs"]:
                if jsonpickle.decode(u).name == club.name:
                    self.raw_data["clubs"][count] = jsonpickle.encode(club)
                count += 1
        else:
            self.raw_data["clubs"].append(jsonpickle.encode(club))

        self.write()

    def get_clubs(self):
        data = copy.deepcopy(self.raw_data)
        count = 0
        for club in self.raw_data["clubs"]:
            data["clubs"][count] = jsonpickle.decode(club)
            count += 1
        return data["clubs"]

    def get_club(self, club_name):
        logging.info("Getting club: " + club_name)

        for club in self.get_clubs():
            if club.name == club.name:
                logging.info("Club found: " + club)
                return club

        logging.info("Club not found: " + club_name)

    def write(self):
        logging.info("Writing to database.")
        file = open(DatabaseHandler._databaseLocation, "w")
        json.dump(self.raw_data, file, sort_keys=True, indent=4)
        file.close()

    @staticmethod
    def get_instance():
        if DatabaseHandler._instance is None:
            DatabaseHandler._instance = DatabaseHandler()
            return DatabaseHandler._instance
        else:
            return DatabaseHandler._instance
