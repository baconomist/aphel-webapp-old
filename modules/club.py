class Club(object):
    def __init__(self, admins, name, description, tags):
        self.admins = admins

        self.name = ""
        self.description = ""
        self.users = []
        self.tags = []
