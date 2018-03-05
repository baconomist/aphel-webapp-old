from flask import Flask, render_template, request, redirect
import logging

from modules.database_handler import DatabaseHandler

# Comment out this line to disable logging
logging.basicConfig(filename='server.log', level=logging.DEBUG)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

databaseHandler = DatabaseHandler()


if __name__ == "__main__":
    app.run("127.0.0.1", 80, debug=True)