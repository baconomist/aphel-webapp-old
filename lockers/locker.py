class Locker(object):
    def __init__(self, id, size=0.25, isTaken=False, student=None, homeroom=None):
        self.id = id
        self.size = size
        self.isTaken = isTaken
        self.student = student
        self.homeroom = homeroom
