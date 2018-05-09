from modules.database_handler import DatabaseHandler
from modules.request_handler import Helper
from modules.teacher import Teacher
from modules.user import User

#user = DatabaseHandler.get_instance().get_user("baconomist@gmail.com")
#user.students = ["623609@pdsb.net"]
#DatabaseHandler.get_instance().store_user(user)


#user = DatabaseHandler.get_instance().get_user("baconomist@gmail.com")
#user = User("baconomist@gmail.com", "")
#user.password = Helper.hash_password("12345678")
#DatabaseHandler.get_instance().store_user(user)
#print(Helper.check_password(DatabaseHandler.get_instance().get_user("baconomist@gmail.com").password, "12345678"))
