from modules.database_handler import DatabaseHandler
user = DatabaseHandler.get_instance().get_user("623609@pdsb.net")
user.announcements=[]
DatabaseHandler.get_instance().store_user(user)