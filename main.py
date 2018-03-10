from flask import Flask, render_template, request, redirect

from modules.request_handler import RequestHandler

import os
import logging
# Clear server.log
open(os.path.join(__file__, "..\\server.log"), "w").close()

# Comment out these lines to disable logging

logging.basicConfig(filename=os.path.join(__file__, "..\\server.log"), level=logging.DEBUG)
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
        return request_handler.login(request)
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        return request_handler.signup(request)
    return render_template("sign_up.html")


if __name__ == "__main__":
    app.run("127.0.0.1", 80, debug=True)
