from flask import Flask, render_template, session

from modules.database_handler import DatabaseHandler
from modules.request_handler import RequestHandler

from html_modules.navbar import Navbar

import config

import os
import logging

# Clear server.log
open(os.path.join(os.path.dirname(__file__), "server.log"), "w").close()

# Comment out these lines to disable logging

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), "server.log"), level=logging.DEBUG)
rootLogger = logging.getLogger()
consoleHandler = logging.StreamHandler()
rootLogger.addHandler(consoleHandler)

app = Flask(__name__)

# Secret key needed for flask-sessions
app.secret_key = os.urandom(24)

request_handler = RequestHandler()


@app.route("/", methods=["POST"])
def catch_all():
    return request_handler.handle_request()


@app.route("/file_upload", methods=["POST"])
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
def profile():
    return render_template("profile.html")


# Then have specific rules for specific html files/links
@app.route("/login", methods=["GET"])
@app.route("/login.html", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/logout", methods=["GET"])
@app.route("/logout.html", methods=["GET"])
def logout():
    session.pop("uid")
    return render_template("logout.html")


@app.route("/signup", methods=["GET"])
@app.route("/signup.html", methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route("/post_announcement", methods=["GET"])
@app.route("/post_announcement.html", methods=["GET"])
def announcement():
    return render_template("post_announcement.html")


@app.route("/dashboard", methods=["GET"])
@app.route("/dashboard.html", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


@app.route("/user_announcements", methods=["GET"])
@app.route("/user_announcements.html", methods=["GET"])
def user_announcements():
    return render_template("user_announcements.html")


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
def students():
    return render_template("students.html")


@app.route("/add_student", methods=["GET"])
@app.route("/add_student.html", methods=["GET"])
def add_student():
    student_uids = []
    for user in DatabaseHandler.get_instance().get_users():
        if user.permission_level < user.get_teacher_permisison_level():
            student_uids.append(user.uid)

    return render_template("add_student.html", student_uids=student_uids)


@app.route("/add_student_status", methods=["GET"])
@app.route("/add_student_status.html", methods=["GET"])
def add_student_status():
    return render_template("add_student_status.html")


@app.context_processor
def inject_navbar():
    navbar = Navbar()
    return dict(navbar=navbar.get_markup())


if __name__ == "__main__":
    app.run(config.ip, config.port, debug=config.DEBUG)
