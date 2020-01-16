import os
import datetime
from datetime import date

from helpers import apology
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


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



@app.route("/", methods=["GET", "POST"])
def index():
    """Show start screen for website"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "GET":
        roominfo = db.execute("SELECT * FROM rooms")
        roomnames = [item["room"] for item in roominfo]
        return render_template("index.html", rooms=roomnames, info=roominfo)
    else:
        # get var
        username = request.form.get("username")
        room = request.form.get("room")

        print(username, room)

        if not username:
            return apology("Voer een gebruikersnaam in", 400)

        if not room:
            return apology("Voer een room in", 400)

        if room == "standard":
            return apology("Kies een room", 400)



        usernames = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if usernames == 1:
            return apology("Gebruikersnaam is al gebruikt")

        # create table users
        db.execute("INSERT INTO users (username, room) VALUES (:username, :room)",
                    username=username, room=room)
        # update useramount in that room
        db.execute("UPDATE rooms SET useramount = useramount + 1 WHERE room= :roomname",
                    roomname=room)
        return inroom()



@app.route("/makeroom", methods=["GET", "POST"])
def makeroom():
    """Show start screen for website"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "GET":
        return render_template("makeroom.html")

    # User reached route via POST
    else:
        # Get all variables
        roomname = request.form.get("room")
        questions = request.form.get("questions")
        username = request.form.get("username")

        # Check if valid answer
        if not roomname and not username:
            return apology("Vul alles in om verder te gaan.")
        if not roomname:
            return apology("Vul een kamernaam in.")

        if questions == "vragen":
            return apology("Kies het aantal vragen.")

        if not username:
            return apology("Vul een gebruikersnaam in.")

        # Insert room into rooms table
        db.execute("INSERT INTO rooms (room, useramount, dates, questions) VALUES(:room, :useramount, :date , :q)",
                    room=roomname, useramount=1, date=date.today(), q=int(questions))

        # Insert user into users table
        db.execute("INSERT INTO users (username, room, fifty, double, joker, score, ready) VALUES(:name, :room, :f, :d, :j, :s, :r)",
                    name=username, room=roomname, f=1, d=1, j=1, s=1, r=0)
        return inroom(True)


@app.route("/room", methods=["GET", "POST"])
def inroom(host=False):
    # Check if user is host of game
    if host == True:
        host = "yes"
        message = "Jij bent momenteel host van deze kamer. \n Jij kiest dus wanneer het spel begint."
        title = "Wachten op medespelers"
    else:
        host = "no"
        message = "De host bepaald wanneer het spel start. Wanneer de host het spel start ga je automatisch naar het spel."
        title = "Wachten totdat de host het spel start."
    username = request.form.get("username")
    room = (db.execute("SELECT room FROM users WHERE username=:user", user=username))[0]["room"]
    print("USERNAME REQUEST: ", username)
    print("ROOM REQUEST: ", room)

    if request.method == "GET":
        print("METHOD GET")
        return render_template("room.html", user=username, room=room, message=message, top=title, host=host)
    else:
        print("METHOD POST")
        return render_template("room.html", user=username, room=room, message=message, top=title, host=host)


@app.route("/thanks", methods=["GET"])
def thanks():
    if request.method == "GET":
        return render_template("thanks.html")
    else:
        return index()
