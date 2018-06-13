from modules.database_handler import DatabaseHandler
from modules.review import Review


class AnnouncementReviewHandler(object):
    _instance = None

    def __init__(self):
        self.unconfirmed_reviews = []

    # update this to take maybe both teacher name and email into consideration
    def new_announcement_review(self, teacher_email, announcement):
        teacher = DatabaseHandler.get_instance().get_user(teacher_email)
        student = DatabaseHandler.get_instance().get_user(announcement.user_name)

        review = Review(teacher, student, announcement)

        self.unconfirmed_reviews.append(review)
        print(self.unconfirmed_reviews)
        return review

    def validate_review(self, review_id):
        copy = []

        for review in self.unconfirmed_reviews:
            copy.append(review)

        for review in copy:
            if review.id == review_id:
                review.student._announcements.append(review.announcement)
                DatabaseHandler.get_instance().store_user(review.student)
                return True

        return False

    @staticmethod
    def get_instance():
        if AnnouncementReviewHandler._instance is None:
            AnnouncementReviewHandler._instance = AnnouncementReviewHandler()
            return AnnouncementReviewHandler._instance
        else:
            return AnnouncementReviewHandler._instance
