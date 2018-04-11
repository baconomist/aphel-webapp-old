from flask import Flask, render_template, request, redirect

from modules.request_handler import RequestHandler

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

'''
# Redirect to any html file
@app.route("/", defaults={"path": ""})
@app.route('/<path:path>')
def catch_all(path):
    if ".html" in path:
        try:
            return all_special_redirects[path.replace(".html", "")]()
        except Exception:
            return render_template(path)
        except:
            return "404 error not found!"
    else:
        return render_template("index.html")
all_special_redirects = {"login": login, "signup": signup}
'''

request_handler = RequestHandler()


@app.route("/", methods=["GET", "POST"])
@app.route("/home")
@app.route("/index")
@app.route("/index.html")
def index():
    if request.method == "POST":
        return request_handler.handle_abstract()
    return render_template("index.html")


# Then have specific rules for specific html files/links
@app.route("/login", methods=["GET", "POST"])
@app.route("/login.html", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return request_handler.login()
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
@app.route("/signup.html", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        return request_handler.signup()
    return render_template("signup.html")

@app.route("/announcement", methods=["GET", "POST"])
@app.route("/announcement.html", methods=["GET", "POST"])
def announcement():
    if request.method == "POST":
        return request_handler.announcement()
    return render_template("announcement.html")

@app.route("/dashboard", methods=["GET", "POST"])
@app.route("/dashboard.html", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        return request_handler.dashboard()
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run("127.0.0.1", 80, debug=True)
