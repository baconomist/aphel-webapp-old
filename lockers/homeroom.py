class Homeroom(object):
    def __init__(self, id, locker_data, class_list, lockers=None):
        if lockers is None:
            lockers = []
        self.id = id
        self.class_list = class_list
        self.lockers = lockers
        self.size = len(class_list)
        self.locker_data = locker_data