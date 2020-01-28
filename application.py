import os
import datetime
from datetime import date
import json
import random

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

    # Remove all gamerooms older than 1 day
    currentdate = str(date.today())
    db.execute("DELETE FROM rooms WHERE dates != :now", now=currentdate)

    if request.method == "GET":

        # Select roomgames which haven't been started yet
        roominfo = db.execute("SELECT * FROM rooms WHERE ready=:status", status=0)
        roomnames = [item["room"] for item in roominfo]
        return render_template("index.html", rooms=roomnames, info=roominfo)
    else:
        # Save user and room
        username = request.form.get("username")
        room = request.form.get("room")

        session["user"] = username
        session["room"] = room

        # Check if form has been filled in correctly
        if not username:
            return apology("Voer een gebruikersnaam in", 400)

        if not room:
            return apology("Voer een room in", 400)

        if room == "standard":
            return apology("Kies een room", 400)


        # Check if username already exists
        usernames = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if usernames:
            return apology("Gebruikersnaam wordt al gebruikt, ga terug en kies een andere naam om te spelen.")

        # Save username to database
        db.execute("INSERT INTO users (username, room) VALUES (:username, :room)",
                    username=username, room=room)

        # Update useramount in that room
        db.execute("UPDATE rooms SET useramount = useramount + 1 WHERE room= :roomname",
                    roomname=room)
        return inroom()



@app.route("/makeroom", methods=["GET", "POST"])
def makeroom():
    """Show start screen for website"""

    if request.method == "GET":
        return render_template("makeroom.html")

    # User reached route via POST
    else:
        # Request chosen category
        number = int(request.form.get("category"))

        # Choose random question within category
        if number == 0:
            index = random.randint(0,4)
        if number == 1:
            print("CORRECT")
            index = random.randint(5,9)
        if number == 2:
            index = random.randint(10,14)
        if number == 3:
            index = random.randint(15,19)

        # Get all variables
        roomname = request.form.get("room")
        questions = request.form.get("questions")
        username = request.form.get("username")

        # Save session
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

        # Check if username already exists
        usernames = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if usernames:
            return apology("Gebruikersnaam wordt al gebruikt, ga terug en kies een andere naam om te spelen.")

        # Check if roomname already exists
        roomnames = db.execute("SELECT * FROM rooms WHERE room = :roomname", roomname=roomname)
        if roomnames:
            return apology("Kamernaam al in gebruik. Ga terug en kies een andere naam om te spelen!")

        # Insert room with questionindex for first question
        db.execute("INSERT INTO rooms (room, useramount, dates, questions, nextindex) VALUES(:room, :useramount, :date, :q, :index)",
                    room=roomname, useramount=1, date=date.today(), q=int(questions), index=index)

        # Insert user into users table
        db.execute("INSERT INTO users (username, room, fifty, double, joker, score, ready) VALUES(:name, :room, :f, :d, :j, :s, :r)",
                    name=username, room=roomname, f=1, d=1, j=1, s=1, r=0)
        return inroom()


@app.route("/room", methods=["GET", "POST"])
def inroom():
    # Return template with message
    return render_template("room.html", user=session["user"], room=session["room"])

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

    # User scores
    room=session["room"]
    getinfo = db.execute("SELECT username, score FROM users WHERE room=:room", room=room)
    info = dict()
    for item in getinfo:
        user = item["username"]
        score = item["score"]
        info[user] = score


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

    return render_template("game.html", user=session["user"], room=session["room"], questions=questions, amount=questionamount, scores=info)



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
    getinfo = db.execute("SELECT username, score FROM users WHERE room=:room", room=request.args.get("room"))
    info = dict()
    for item in getinfo:
        user = item["username"]
        score = item["score"]
        info[user] = score

    return jsonify(info)


@app.route("/updatescore")
def updatescore():
    user = request.args.get("user")
    update = request.args.get("update")
    print(user, update)
    db.execute("UPDATE users SET score = :update WHERE username=:user", update=update, user=user)
    return update

@app.route("/getuserscore")
def userscore():
    user = request.args.get("userscore")
    score = db.execute("SELECT score FROM users WHERE username=:user", user=user)
    userscore=score["score"]
    return jsonify(userscore)

@app.route("/question")
def question():
    # Choose questions with chosen category
    number = int(request.args.get("cat"))


    # Choose random question within category
    if number == 0:
        index = random.randint(0,4)
    if number == 1:
        index = random.randint(5,9)
    if number == 2:
        index = random.randint(10,14)
    if number == 3:
        index = random.randint(15,19)

    # Set question index in database
    db.execute("UPDATE rooms SET nextindex = :index", index=index)

    # Return question index
    return jsonify(index)

@app.route("/checkquestion")
def checkquestion():
    # Select room
    room = request.args.get("room")
    row = db.execute("SELECT * FROM rooms WHERE room = :room", room=room)


    # Select index of next question
    index = row[0]["nextindex"]
    print("INDEX: ", index)


    # Return question index

    return jsonify(index)


@app.route("/ranking", methods=["GET", "POST"])
def ranking():
    if request.method == "GET":

        # get used room
        room = session["room"]

        # get username and score using room out of db
        ranking = db.execute("SELECT username, score FROM users WHERE room = :room", room=room)

        # sort dict using reverse
        sortedranking = sorted(ranking, key=lambda x: int(x['score']), reverse=True)
        user=session["user"]
        print(user)
        # add ranking to dict
        j = 1
        for i in sortedranking:
                i["rank"] = j
                j += 1

        # give dict to html
        return render_template("ranking.html", ranking=sortedranking, user=session["user"])




@app.route("/lost", methods=["GET", "POST"])
def lost():
    if request.method == "GET":
        return render_template("lost.html")
    if request.method == "POST":

        reviews = request.form.get("review")
        db.execute("UPDATE users SET review = :review WHERE username = :user",
        review = reviews, user=session["user"])
        print(review)
        return render_template("lost.html")


@app.route("/review", methods=["GET", "POST"])
def review():
    if request.method == "GET":
        getinfo = db.execute("SELECT username, review FROM users")
        print(getinfo)
        return render_template("review.html", reviews=getinfo)





@app.route("/final", methods=["GET", "POST"])
def final():
    # Get information of room
    room=session["room"]
    getinfo = db.execute("SELECT username, score FROM users WHERE room=:room", room=room)
    info = dict()
    for item in getinfo:
        user = item["username"]
        score = item["score"]
        info[user] = score
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

    return render_template("final.html", user=session["user"], scores=info, room=session["room"], questions=questions, amount=questionamount)

@app.route("/finalroom", methods=["GET", "POST"])
def finalroom():
    return render_template("finalroom.html")


@app.route("/winner", methods=["GET", "POST"])
def winner():
     if request.method == "GET":
         return render_template("winner.html")

@app.route("/userready")
def userready():
    arg = request.args.get("arg")
    usr = session["user"]
    print("USER: ", usr)

    # Set user ready for game
    if arg == "set":
        db.execute("UPDATE users SET ready = :ready WHERE username = :user", ready=1, user=usr)
        return jsonify(True)

    # Check if all users are ready for game
    if arg == "check":
        users = db.execute("SELECT * FROM users WHERE room=:room", room=session["room"])
        users_ready = db.execute("SELECT * FROM users WHERE ready=:ready AND room=:room", ready=1, room=session["room"])

        # If all users are ready to play
        if len(users) == len(users_ready):
            print("READY")
            return jsonify(True)

        # If not
        else:
            print(users)
            print("ready:", len(users_ready), "users:", len(users))
            print("NOT READY")
            return jsonify(False)

    if arg == "reset":
        db.execute("UPDATE users SET ready = :ready WHERE username =:user", ready=0, user=usr)
        return jsonify(True)

    if arg == "checkfinal":
        users_ready = db.execute("SELECT * FROM users WHERE ready=:ready AND room=:room", ready=1, room=session["room"])

        if len(users_ready) == 2:
            return jsonify(True)
        else:
            return jsonify(False)





