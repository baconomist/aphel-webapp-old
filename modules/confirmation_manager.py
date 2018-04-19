from modules.confirmation import Confirmation
from modules.database_handler import DatabaseHandler

class ConfirmationManager(object):

    _instance = None

    def __init__(self):
        self.unconfirmed_users = {}

    def new_confirmation(self, user):
        self.unconfirmed_users[user] = Confirmation()
        return self.unconfirmed_users[user]

    def validate_confirmation(self, confirmation_id):
        copy = {}
        for key in self.unconfirmed_users.keys():
            copy[key] = self.unconfirmed_users[key]

        for user in copy.keys():
            confirmation = copy[user]
            if confirmation.id == confirmation_id and confirmation.is_valid():
                user.confirmed = True
                DatabaseHandler.get_instance().store_user(user)
                del self.unconfirmed_users[user]
                return True
            elif not confirmation.is_valid():
                DatabaseHandler.get_instance().remove_user(user.uid)
                del self.unconfirmed_users[user]
                return False

        return False

    @staticmethod
    def get_instance():
        if ConfirmationManager._instance is None:
            ConfirmationManager._instance = ConfirmationManager()
            return ConfirmationManager._instance
        else:
            return ConfirmationManager._instance





