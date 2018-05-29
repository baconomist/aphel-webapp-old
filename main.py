from flask import Flask, render_template, request, redirect
from flask_cors import cross_origin

from modules.request_handler import RequestHandler

from html_modules.navbar import NavBar

import config

import os
import logging
from flask import jsonify

# Clear server.log
open(os.path.join(os.path.dirname(__file__), "server.log"), "w").close()

# Comment out these lines to disable logging

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), "server.log"), level=logging.DEBUG)
rootLogger = logging.getLogger()
consoleHandler = logging.StreamHandler()
rootLogger.addHandler(consoleHandler)

app = Flask(__name__)

request_handler = RequestHandler()

'''
    cross origin for testing
'''


def debug_cross_origin(decorator):
    return decorator if config.DEBUG else lambda x: x


#@app.route("/debug", methods=["POST"])
#@cross_origin(origin="*")
#def debug():
    #return jsonify(data=config.DEBUG)


@app.route("/", methods=["POST"])
@debug_cross_origin(cross_origin(origin="*"))
def catch_all():
    return request_handler.handle_request()


@app.route("/file_upload", methods=["POST"])
@debug_cross_origin(cross_origin(origin="*"))
def file_upload():
    return request_handler.handle_file_upload()


'''
    cross origin for testing
'''


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
    return render_template("add_student.html", navbar=NavBar().markup)


@app.route("/add_student_status", methods=["GET"])
@app.route("/add_student_status.html", methods=["GET"])
def add_student_status():
    return render_template("add_student_status.html")


if __name__ == "__main__":
    app.run(config.ip, config.port, debug=config.DEBUG)
