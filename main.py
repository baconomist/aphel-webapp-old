from flask import Flask, render_template, request, redirect
import logging
import json, jsonpickle

from modules.database_handler import DatabaseHandler
from modules.user import User

# Comment out these lines to disable logging
logging.basicConfig(filename='server.log', level=logging.DEBUG)
rootLogger = logging.getLogger()
consoleHandler = logging.StreamHandler()
rootLogger.addHandler(consoleHandler)

app = Flask(__name__)

database_handler = DatabaseHandler()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        try:
            data = request.form.getlist("user[]")
            database_handler.store_user(User(data[0], data[1]))
        except:
            pass
        return "Success"
    elif "all_users" in request.args:
        return json.dumps(database_handler.raw_data)
    elif "get_user" in request.args:
        return jsonpickle.encode(database_handler.get_user(request.args["get_user"]))
    else:
        return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run("127.0.0.1", 80, debug=True)
