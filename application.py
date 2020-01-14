import os
import datetime

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# from helperes import update_database



# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///webproject.db")


# Put questions in database


@app.route("/", methods=["GET", "POST"])
def index():
    """Show start screen for website"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "GET":
        rooms = db.execute("SELECT room FROM rooms")
        return render_template("index.html", rooms=rooms)
    else:
        # get var
        username = request.form.get("username")
        room = request.form.get("room")

        # create table users
        db.execute("INSERT INTO users (username, room) VALUES (:username, :room)",
                    username=username, room=room)
        db.execute("UPDATE room SET useramount +=1 WHERE room = :room",
                    room=room)
        return render_template("room.html")



@app.route("/makeroom", methods=["GET", "POST"])
def makeroom():
    """Show start screen for website"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "GET":
        return render_template("index.html")

    # User reached route via POST
    else:
        roomname = request.form.get("room")
        db.execute("INSERT INTO rooms (room, useramount, dates VALUES(:room, :useramount, :date)", room=roomname, useramount=0, date=datetime.datetime.now())

        return index()

@app.route("/thanks", methods=["GET"])
def thanks():
    if request.method == "GET":
        return render_template("thanks.html")
    else:
        return index()
