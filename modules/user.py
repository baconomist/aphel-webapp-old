from modules.announcement import Announcement
import json

class User(object):
    def __init__(self, uid, password):
        self.uid = uid
        self.password = password
        self.permission_level = 0
        self._announcements = []
        self.confirmed = False

        self.profile_image = None
        self.firstname = ""
        self.lastname = ""
        self.clubs = []

    def create_announcement(self, title: str, info: str, content_html: str, id: int):
        # if for some reason user has no attribute "self.announcements"
        try:
            self.get_announcement_by_id(id).title = title
            self.get_announcement_by_id(id).info = info
            self.get_announcement_by_id(id).content_html = content_html
        except:
            self._announcements.append(Announcement(title=title, info=info, content_html=content_html, user_name=self.uid, id=id))

    def remove_announcement_by_id(self, id):
        copy = []
        for announcement in self._announcements:
            copy.append(announcement)

        index = 0
        for announcement in copy:
            if announcement.id == id:
                self._announcements.pop(index)
                break
            index += 1

    def get_announcement_by_id(self, id):
        for announcement in self._announcements:
            if announcement.id == id:
                return announcement
        return None

    def announcement_exists(self, announcement_e):
        for announcement in self._announcements:
            if announcement.id == announcement_e.id:
                return True
        return False

    def get_profile_info_json(self):
        return json.dumps({"firstname": self.firstname, "lastname": self.lastname, "clubs": self.clubs})

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

    @staticmethod
    def get_teacher_permisison_level():
        return 3

    @staticmethod
    def get_trusted_student_permission_level():
        return 2

    @staticmethod
    def get_untrusted_student_permission_level():
        return 1

    @staticmethod
    def get_new_student_permission_level():
        return 0
