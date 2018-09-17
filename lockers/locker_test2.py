import string, random, json, math
from lockers.locker import Locker
from lockers.homeroom import Homeroom

lockers = []
for i in range(378, 480):
    lockers.append(Locker(i))


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

def getNewHomeroomInstance(homeroom: int):
    try:
        return Homeroom(homeroom, json.load(open("locker_data.json"))[str(homeroom)],
                        json.load(open("classes.json"))[str(homeroom)])
    except KeyError:
        print("Error, Possibly no such homeroom: " + str(homeroom))


def getHomerooms():
    homerooms = []
    for homeroom in json.load(open("classes.json")):
        homerooms.append(getNewHomeroomInstance(homeroom))
    return homerooms

lockers = []
for i in range(215, 480):
    lockers.append(Locker(i))

homerooms = getHomerooms()

for i in range(2):
    potential_lockers = []
    end_locker_id = -1
    for locker in lockers:
        if not locker.id >= end_locker_id or end_locker_id == -1:
            if not locker.isTaken:
                potential_lockers.append(locker)
                for homeroom in homerooms:
                    if homeroom.locker_data[0] == locker.id:
                        end_locker_id = potential_lockers[-1].id + (homeroom.size - (potential_lockers[-1].id - potential_lockers[0].id))
        else:
            break

    for locker in potential_lockers:
        locker.isTaken = True
        #print(locker.id)




