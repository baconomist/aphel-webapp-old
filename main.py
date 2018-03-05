from flask import Flask, render_template, request, redirect
import logging
import json

from modules.database_handler import DatabaseHandler

# Comment out this line to disable logging
logging.basicConfig(filename='server.log', level=logging.DEBUG)

app = Flask(__name__)
database_handler = DatabaseHandler()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print(request)
        return ""
    elif "all_users" in request.args:
        return json.dumps(database_handler.raw_data)
    else:
        return render_template("index.html")




@app.route("/login")
def login():
    return render_template("login.html")



if __name__ == "__main__":
    app.run("127.0.0.1", 80, debug=True)