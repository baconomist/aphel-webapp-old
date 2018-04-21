from flask import Flask, render_template, request, redirect

from modules.request_handler import RequestHandler
from modules.server import Server


import os
import logging
import inspect

# Clear server.log
open(os.path.join(__file__, "..\\server.log"), "w").close()

# Comment out these lines to disable logging

logging.basicConfig(filename=os.path.join(__file__, "..\\server.log"), level=logging.DEBUG)
rootLogger = logging.getLogger()
consoleHandler = logging.StreamHandler()
rootLogger.addHandler(consoleHandler)

app = Flask(__name__)

request_handler = RequestHandler()


@app.route("/", methods=["POST"])
def catch_all():
    return request_handler.handle_request()


@app.route("/", methods=["GET"])
@app.route("/home")
@app.route("/index")
@app.route("/index.html")
def index():
    return render_template("index.html")


# Then have specific rules for specific html files/links
@app.route("/login", methods=["GET"])
@app.route("/login.html", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/signup", methods=["GET"])
@app.route("/signup.html", methods=["GET"])
def signup():
    return render_template("signup.html")


@app.route("/announcement", methods=["GET"])
@app.route("/announcement.html", methods=["GET"])
def announcement():
    return render_template("announcement.html")


@app.route("/dashboard", methods=["GET"])
@app.route("/dashboard.html", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")


@app.route("/edit_announcements", methods=["GET"])
@app.route("/edit_announcements.html", methods=["GET"])
def user_announcements():
    return render_template("edit_announcements.html")


@app.route("/confirmation", methods=["GET"])
def confirmation():
    return render_template("confirmation.html")


if __name__ == "__main__":
    app.run(Server.ip, 80, debug=True)
