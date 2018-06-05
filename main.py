from functools import wraps

from flask import Flask, render_template, session, abort, url_for

from html_modules.announcement_form import AnnouncementForm
from html_modules.editable_announcement import EditableAnnouncement
from html_modules.student_template import StudentTemplate
from modules.database_handler import DatabaseHandler
from modules.request_handler import RequestHandler, Helper

from html_modules.navbar import Navbar

import config

import os
import logging

# Clear server.log
from modules.student import Student
from modules.teacher import Teacher
from modules.user import User

open(os.path.join(os.path.dirname(__file__), "server.log"), "w").close()

# Comment out these lines to disable logging

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), "server.log"), level=logging.DEBUG)
rootLogger = logging.getLogger()
consoleHandler = logging.StreamHandler()
rootLogger.addHandler(consoleHandler)

app = Flask(__name__)

# Secret key needed for flask-sessions
app.secret_key = os.urandom(24)


def page_not_found(e):
    return render_template("errors/404.html"), 404


def no_access(e):
    return render_template("errors/403.html"), 403


# 404 page, page not found
app.register_error_handler(404, page_not_found)

# 403 page, not logged in/can't access resource
app.register_error_handler(403, no_access)

request_handler = RequestHandler()


def login_required(flask_route_function):
    @wraps(flask_route_function)
    def wrapper(*args, **kwargs):
        if session.get("uid") is None:
            abort(403)
        return flask_route_function(*args, **kwargs)

    return wrapper


@app.route("/", methods=["POST"])
def catch_all():
    return request_handler.handle_request()


@app.route("/file_upload", methods=["POST"])
@login_required
def file_upload():
    return request_handler.handle_file_upload()


@app.route("/", methods=["GET"])
@app.route("/home")
@app.route("/index")
@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/profile", methods=["GET"])
@app.route("/profile.html", methods=["GET"])
@login_required
def profile():
    user = DatabaseHandler.get_instance().get_user(session.get("uid"))

    image_url = ""
    try:
        image_url = url_for("static", filename="data/profile_images/" + user.uid + ".jpg")
    except:
        pass

    print(image_url)

    grade = user.grade if isinstance(user, Student) else ""
    return render_template("profile.html", uid=session.get("uid"),
                           firstname=user.firstname, lastname=user.lastname,
                           grade=grade, image_url=image_url)


# Then have specific rules for specific html files/links
@app.route("/login", methods=["GET"])
@app.route("/login.html", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
@app.route("/logout.html", methods=["GET"])
@login_required
def logout():
    session.pop("uid")
    return render_template("logout.html")


@app.route("/signup", methods=["GET"])
@app.route("/signup.html", methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route("/post_announcement", methods=["GET"])
@app.route("/post_announcement.html", methods=["GET"])
@login_required
def announcement():
    teacher_uids = []
    for user in DatabaseHandler.get_instance().get_users():
        if Helper.is_user_admin(user) or type(user) is Teacher:
            teacher_uids.append(user.uid)
    trusted_post = DatabaseHandler.get_instance().get_user(session.get("uid")).permission_level >= User.get_trusted_student_permission_level()

    announcement_form = AnnouncementForm(trusted_post, len(DatabaseHandler.get_instance().get_user(session.get("uid"))._announcements) + 1, teacher_uids)

    return render_template("post_announcement.html", announcement_form=announcement_form.get_markup())


@app.route("/dashboard", methods=["GET"])
@app.route("/dashboard.html", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


@app.route("/user_announcements", methods=["GET"])
@app.route("/user_announcements.html", methods=["GET"])
@login_required
def user_announcements():
    user_announcements = DatabaseHandler.get_instance().get_user(session.get("uid"))._announcements

    # Sort in chronological order(newest on top, oldest on bottom)
    user_announcements.sort(key=lambda x: x.time_stamp)

    # Have to reverse it for it to work
    user_announcements.reverse()

    editable_announcements = []

    for announcement in user_announcements:
        editable_announcements.append(EditableAnnouncement(announcement).get_markup())

    return render_template("user_announcements.html", user_announcements=editable_announcements)


@app.route("/confirmation", methods=["GET"])
@app.route("/confirmation.html", methods=["GET"])
def confirmation():
    return render_template("confirmation.html")


@app.route("/confirmation_confirmed", methods=["GET"])
def confirmation_confirmed():
    return render_template("confirmation_confirmed.html")


@app.route("/review_confirmed", methods=["GET"])
def review_confirmed():
    return render_template("review_confirmed.html")


@app.route("/students", methods=["GET"])
@app.route("/students.html", methods=["GET"])
@login_required
def students():
    students = []

    for student in DatabaseHandler.get_instance().get_user(session.get("uid")).students:
        student = DatabaseHandler.get_instance().get_user(student)
        students.append(StudentTemplate(student.uid, student.permission_level,
                                        student.firstname + " " + student.lastname).get_markup())

    return render_template("students.html", students=students)


@app.route("/add_student", methods=["GET"])
@app.route("/add_student.html", methods=["GET"])
@login_required
def add_student():
    student_uids = []
    for user in DatabaseHandler.get_instance().get_users():
        if user.permission_level < user.get_teacher_permisison_level():
            student_uids.append(user.uid)

    return render_template("add_student.html", student_uids=student_uids)


@app.route("/add_student_status", methods=["GET"])
@app.route("/add_student_status.html", methods=["GET"])
@login_required
def add_student_status():
    return render_template("add_student_status.html")


@app.context_processor
def inject_navbar():
    navbar = Navbar()
    return dict(navbar=navbar.get_markup())


if __name__ == "__main__":
    app.run(config.ip, config.port, debug=config.DEBUG)
