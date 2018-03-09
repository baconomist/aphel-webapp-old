class User(object):
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.permission_level = 0

    '''
    permission level 0 - can only view posted announcements
    permission level 1 - can post announcements
    permission level 2 - teacher/admin
    '''

    def set_permission_level(self, level):
        assert level < 3, b'Permission level > 3 does not exist!'
        self.permission_level = level

    def get_permission_level(self):
        return self.permission_level
