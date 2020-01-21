import os
import datetime
from datetime import date
import json

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

        # Select roomgames which haven't been started yet
        roominfo = db.execute("SELECT * FROM rooms WHERE ready=:status", status=0)
        roomnames = [item["room"] for item in roominfo]
        return render_template("index.html", rooms=roomnames, info=roominfo)
    else:
        # get var
        username = request.form.get("username")
        room = request.form.get("room")

        session["user"] = username
        session["room"] = room

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

        session["user"] = username
        session["room"] = roomname

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
    # Check if user is host of game and pass message
    if host == True:
        host = "yes"
        message = "Jij bent momenteel host van deze kamer. \n Jij kiest dus wanneer het spel begint."
        title = "Spel starten..."
        warning = "Wanneer jij op SPEL STARTEN klikt wordt de kamer afgesloten en kan er dus niemand meer deelnemen."
    else:
        host = "no"
        title = "Wachten totdat de host het spel start..."
        message = "Momenteel is het mogelijk voor andere spelers om de kamer te betreden. Wanneer de host het spel start wordt de kamer gesloten."
        warning = "Nadat de host op SPEL STARTEN heeft gedrukt kan dit maximaal 5 seconden duren."
    username = request.form.get("username")
    room = (db.execute("SELECT room FROM users WHERE username=:user", user=username))[0]["room"]

    if request.method == "GET":
        return render_template("room.html", user=username, room=room, message=message, top=title, host=host, w=warning)
    else:
        return render_template("room.html", user=username, room=room, message=message, top=title, host=host, w=warning)

@app.route("/setready")
def setready():
    room = request.args.get("room")
    db.execute("UPDATE rooms SET ready=:status WHERE room=:room", status=1, room=room)
    return jsonify(True)

# Check if game is ready to start (selected by host)
@app.route("/check")
def check():
    info = db.execute("SELECT * FROM rooms WHERE room=:room", room=request.args.get("room"))
    ready = info[0]["ready"]

    if ready == 0:
        return jsonify(False)
    else:
        return jsonify(True)



@app.route("/game", methods=["GET", "POST"])
def game():
    # Get information of room
    room=session["room"]
    questionamount = (db.execute("SELECT questions FROM rooms WHERE room=:room", room=room))[0]["questions"]

    # Get questions
    questiondata = db.execute("SELECT * FROM questions")
    questions = []
    for line in questiondata:
        qdict = dict()
        qdict["question"] = line["question"]
        qdict["category"] = line["category"]
        qdict["correct"] = line["correctanswer"]
        qdict["answer2"] = line["answer2"]
        qdict["answer3"] = line["answer3"]
        qdict["answer4"] = line["answer4"]
        qdict["pointscorrect"] = line["pointscorrect"]
        qdict["pointsincorrect"] = line["pointsincorrect"]
        questions.append(qdict)

    return render_template("game.html", user=session["user"], room=session["room"], questions=questions, amount=questionamount)



@app.route("/thanks", methods=["GET"])
def thanks():
    if request.method == "GET":
        return render_template("thanks.html")
    else:
        return index()

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


@app.route("/getscores")
def scores():
    info = db.execute("SELECT username, score FROM users WHERE room=:room", room=request.args.get("room"))
    print(info)
    return jsonify(info)


@app.route("/updatescore")
def updatescore():
    user = request.args.get("user")
    update = request.args.get("update")
    print(user, update)
    db.execute("UPDATE users SET score = :update WHERE username=:user", update=update, user=user)
    return update

