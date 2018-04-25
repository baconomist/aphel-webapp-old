from modules.database_handler import DatabaseHandler


def delete_all_announcements():
    i = input("Are you sure you want to DELETE ALL ANNOUNCEMENTS?(y/n)")
    i2 = input("Are you really sure? This shouldn't be done unless you are ABSOLUTELY SURE!(y/n)")
    if i == "y" and i2 == "y":
        for user in DatabaseHandler.get_instance().get_users():
            user.announcements = []
            DatabaseHandler.get_instance().store_user(user)
    else:
        print("Cancelled Deletion Of All Announcements.")