import string, random, json
from lockers.locker import Locker
from lockers.homeroom import Homeroom


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

lockers = []
for i in range(216, 1000):
    lockers.append(Locker(i))


def getNewHomeroomInstance(homeroom: int):
    try:
        return Homeroom(homeroom, json.load(open("locker_data.json"))[str(homeroom)],
                        json.load(open("classes.json"))[str(homeroom)])
    except KeyError:
        print("Error, Possibly no such homeroom: " + str(homeroom))


def get_start_locker_for_homeroom(homeroom: Homeroom):
    for i in range(homeroom.locker_data[0] - homeroom.size, homeroom.locker_data[1] + 100):
        if lockers[i - lockers[0].id].isTaken:
            continue
        else:
            return i


def assign_lockers(homeroom: Homeroom):
    start_locker = get_start_locker_for_homeroom(homeroom)
    c = 0
    for i in range(start_locker, homeroom.locker_data[1] + homeroom.size):
        if c < homeroom.size:
            list_index = i - lockers[0].id
            lockers[list_index].isTaken = True
            lockers[list_index].student = homeroom.class_list[i - start_locker]
            lockers[list_index].homeroom = homeroom.id
            homeroom.lockers.append(lockers[list_index])
        else:
            break
        c+=1


assign_lockers(getNewHomeroomInstance(136))
assign_lockers(getNewHomeroomInstance(134))
assign_lockers(getNewHomeroomInstance(132))
prev_hr = None
for locker in lockers:
    if prev_hr is not locker.homeroom:
        print("**************************")
    if not locker.student is None:
        print(locker.student, locker.homeroom, locker.id)
    prev_hr = locker.homeroom
# print(get_start_locker_for_homeroom(134, 20, get_locker_data_for_homeroom(134)), get_locker_data_for_homeroom(134))


'''
PSEUDO CODE

SORT BY:
    1. SCI-TECH, STRINGS(Priority)
    2. ALPHABETICALLY

start -> homeroom 1
getHomeroomLockers() -> nearest lockers to homeroom( rm 136 between 457-458)
lastTakenLocker = goBackwardsToFindLastTakenLocker() -> locker_distance <= 10m possibly
fillLockers(lastTakenLocker, class)


class Locker:
    static float width = ~0.25m?
    def isNearHomeroom(hr: int)
        return hr in self.nearest_homerooms
'''
