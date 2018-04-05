from flask import Flask, render_template, request, redirect

from modules.request_handler import *

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


# Then have specific rules for specific html files/links
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return RequestHandler.login(request)
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        return RequestHandler.signup(request)
    return render_template("signup.html")

all_special_redirects = {"login": login, "signup": signup}

if __name__ == "__main__":
    app.run("127.0.0.1", 80, debug=True)
