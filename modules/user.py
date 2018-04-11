from modules.announcement import Announcement


class User(object):
    def __init__(self, uid, password):
        self.uid = uid
        self.password = password
        self.permission_level = 0
        self.announcements = []

    def create_announcement(self, content_html: str, id: int):
        # if for some reason user has no attribute "self.announcements"
        try:
            self.get_announcement_by_id(id).content_html = content_html
        except:
            self.announcements.append(Announcement(content_html=content_html, user_name=self.uid, id=id))

    def get_announcement_by_id(self, id):
        for announcement in self.announcements:
            if announcement.id == id:
                return announcement
        return None

    def announcement_exists(self, announcement_e):
        for announcement in self.announcements:
            if announcement.id == announcement_e.id:
                return True
        return False

    '''
    permission level 0 - can only view posted announcements
    permission level 1 - student can only post announcements with teacher review
    permission level 2 - student can post without teacher announcement review
    permission level 3 - teacher/admin
    '''

    def set_permission_level(self, level):
        assert level < 3, b'Permission level > 3 does not exist!'
        self.permission_level = level

    def get_permission_level(self):
        return self.permission_level
