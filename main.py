from flask import Flask, render_template, request, redirect
import logging
import json, jsonpickle

from modules.database_handler import DatabaseHandler
from modules.request_handler import RequestHandler
from modules.user import User

# Comment out these lines to disable logging
logging.basicConfig(filename='server.log', level=logging.DEBUG)
rootLogger = logging.getLogger()
consoleHandler = logging.StreamHandler()
rootLogger.addHandler(consoleHandler)

app = Flask(__name__)

request_handler = RequestHandler()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        request_handler.login(request)
        return "Success"
    return render_template("login.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        request_handler.sign_up(request)
        return "Success"
    return render_template("sign_up.html")


if __name__ == "__main__":
    app.run("127.0.0.1", 80, debug=True)
