import string
import random
import json
from lockers.locker import Locker
from lockers.homeroom import Homeroom


class LockerManager(object):
    def __init__(self):
        self.lockers = []
        self.homerooms = []
        self.create()

        self.assign_lockers()

    def create(self):
        self.homerooms = self.create_homeroom_instances()
        self.create_lockers()

    def create_lockers(self):
        for i in range(1, 3000):
            self.lockers.append(Locker(i))

    def create_homeroom_instances(self):
        homerooms = []
        class_data = json.load(open("classes.json", "r"))
        for homeroom in class_data:
            hr = Homeroom(int(homeroom), json.load(open("locker_data.json"))[str(homeroom)],
                            class_data[homeroom])
            homerooms.append(hr)
        return homerooms

    ''' Getter Methods '''
    def get_locker_by_id(self, id: int):
        for locker in self.lockers:
            if locker.id == id:
                return locker

    def get_homeroom_by_id(self, id: int):
        for homeroom in self.homerooms:
            if homeroom.id == id:
                return homeroom

    ''' Algorithm '''
    def get_homeroom_fill_start(self, homeroom: Homeroom):
        for i in range(homeroom.locker_data[0] - homeroom.size, homeroom.locker_data[1] + 100):
            if self.get_locker_by_id(i).isTaken:
                continue
            else:
                return self.get_locker_by_id(i)
    def assign_lockers(self):
        for homeroom in self.homerooms:
            start_locker = self.get_homeroom_fill_start(homeroom)
            c = 0
            for i in range(start_locker.id, homeroom.locker_data[1] + homeroom.size):
                if c < homeroom.size:
                    self.get_locker_by_id(i).isTaken = True
                    self.get_locker_by_id(i).student = homeroom.class_list[i - start_locker.id]
                    self.get_locker_by_id(i).homeroom = homeroom.id
                    homeroom.lockers.append(self.get_locker_by_id(i))
                else:
                    break
                c += 1

    ''' Algorithm Correction '''
    def push_back(self, locker: Locker):
        pass
        ''' from this locker space loop through all lockers and homerooms and change locker ids,
        subtract all locker ids by x and remove the empty lockers to create them at the end of the self.lockers array'''

    def fill_push(self):
        # Some lockers are left empty due to algorithm, need to "push" all lockers back to fill empty lockers
        for locker in self.lockers:
            if not locker.isTaken:
                self.push_back(locker)

LockerManager()

'''
def generate_data_file(homerooms: list):
    first_names = ["Lucas", "Jack", "Shrey", "Aryan", "Mahbod"]

    classes = {}
    for hr in homerooms:
        classes[hr] = []
        for i in range(random.randint(10, 20)):
            classes[hr].append(
                first_names[random.randint(0, len(first_names) - 1)] + " " + random.choice(
                    string.ascii_uppercase) + ".")

    # print(classes)
    file = open("classes.json", "w")
    json.dump(classes, file, indent=4, sort_keys=True)
    file.close()


# generate_data_file([132, 134, 136])
'''
