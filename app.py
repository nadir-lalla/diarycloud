import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from collections import Counter

from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///user.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

##############
#     INDEX
##############
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Cover page of word map"""
    userid = db.execute("SELECT name FROM users WHERE id = ?;", session['user_id'])[0]['name'].capitalize()

    if request.method == "GET":

        date = datetime.now()
        month = date.month
        year = date.year

        try:
            text_db = db.execute("SELECT mood, notes, text FROM userdata WHERE user_id=? AND month=? AND year=?;",session['user_id'],month,year)
        except:
            text_db = "No text found from GET"

    if request.method == "POST":
        month = request.form.get('month')
        year = request.form.get('year')

        try:
            text_db = db.execute("SELECT mood, notes, text FROM userdata WHERE user_id=? AND month=? AND year=?;",session['user_id'],month,year)
        except:
            text_db = "No text found from POST"


    text_string = ''
    for entry in text_db:
        for value in entry.values():
            if value is not None:
                text_string += str(value) + ' '

    if len(text_string) == 0:
        text_string = "Welcome to your WordCloud Diary"


    return render_template("index.html", name=userid, text_db=text_string)


##############
#     DIARY
##############
@app.route("/diary", methods=["GET", "POST"])
@login_required
def diary():
    """Page to input your thoughts"""
    userid = db.execute("SELECT name FROM users WHERE id = ?;", session['user_id'])[0]['name'].capitalize()

    if request.method == "POST":
        entry = request.form.get('entry')
        mood = " ".join(request.form.getlist('mood'))

        print(entry)
        print(mood)

        if not entry and not mood:
            return render_template("diary.html", name=userid, apology="No diary or mood entry")

        try:
            date = datetime.strptime(request.form.get('date'), "%Y-%m-%d").date()
        except:
            date = datetime.now()

        day = date.day
        month = date.month
        year = date.year
        print(day, month, year)

        date_db = db.execute("SELECT * FROM userdata WHERE day = ? AND month = ? AND year = ?;", day, month, year)
        print("DB LEN: ", len(date_db))

        if len(date_db) == 0:

            # If no text or mood for the day. Add to db
            db.execute("INSERT INTO userdata (text, user_id, day, month, year, mood) VALUES (?);", (entry, session["user_id"], day, month, year, mood))

        else:
            if entry and not mood:
                # print("Entry and no mood")
                if not date_db[0]['text']:
                    db.execute("UPDATE userdata SET text = ? WHERE day = ? AND month = ? AND year = ?;", entry, day, month, year)
                else:
                    db.execute("INSERT INTO userdata (text, user_id, day, month, year) VALUES (?);", (entry, session["user_id"], day, month, year))
            elif mood and not entry:
                # print("Mood and no entry")
                if not date_db[0]['mood']:
                    db.execute("UPDATE userdata SET mood = ? WHERE day = ? AND month = ? AND year = ?;", mood,day, month, year)
                else:
                    db.execute("INSERT INTO userdata (mood, user_id, day, month, year) VALUES (?);", (mood, session["user_id"], day, month, year))
            else:
                # print('both entry and mood')
                db.execute("INSERT INTO userdata (mood, text, user_id, day, month, year) VALUES (?);", (mood, entry, session["user_id"], day, month, year))

    return render_template("diary.html", name=userid)


#########################
#     NOTES AND IMAGE
#########################
@app.route("/images", methods=["GET", "POST"])
@login_required
def images():
    """Page to input your thoughts"""
    userid = db.execute("SELECT name FROM users WHERE id = ?;", session['user_id'])[0]['name'].capitalize()

    if request.method == "POST":
        note = request.form.get('note')
        img = request.form.get("img")

        if not note and not img:
            return render_template("images.html", name=userid, apology="No entry found")

        try:
            date = datetime.strptime(request.form.get('date'), "%Y-%m-%d").date()
        except:
            date = datetime.now()

        if not img:
            img = False

        day = date.day
        month = date.month
        year = date.year
        print("DD MM YYYY:  ",day, month, year,"\nNote: ",note,"\nimg Name: ", img )

        db.execute("INSERT INTO userdata (image, notes, user_id, day, month, year) VALUES (?);", (img, note, session["user_id"], day, month, year))

    return render_template("images.html", name=userid)




################################
#     LOGIN, LOGOUT, REGISTER
################################
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("apology.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Clear any exisiting user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("password")
        confirm = request.form.get("confirmation")

        if not username:
            return render_template("apology.html")
        if not name:
            return render_template("apology.html")
        elif not password:
            return render_template("apology.html")
        elif not confirm:
            return render_template("apology.html")
        elif password != confirm:
            return render_template("apology.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        count = len(rows)

        if count != 0:
            return render_template("apology.html")

        # Enter into db
        db.execute(
            "INSERT INTO users (username, hash, name) VALUES (?);",
            (username, generate_password_hash(password), name),
        )

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("register.html")

