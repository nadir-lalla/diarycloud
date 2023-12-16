import calendar
from datetime import datetime
from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import re

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

#######################
#     INDEX
##      QUICK ENTRY
#######################
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Cover page of word map"""
    userid = db.execute("SELECT name FROM users WHERE id = ?;", session['user_id'])[0]['name']
    apology = ""
    # print(userid)

    if request.method == "GET":
        date = datetime.now()
        year = date.year

        try:
            text_db = db.execute("SELECT mood, text FROM userdata WHERE user_id=? AND year=?;",session['user_id'],year)
        except:
            text_db = "No entries found"

        text_string = ''
        for entry in text_db:
            for value in entry.values():
                if value and value is not None:
                    # Convert the value to string and remove all punctuations
                    text_string += re.sub(r'[^\w\s]', '', str(value)) + ' '

        if len(text_string) == 0:
            text_string = "Welcome to your WordCloud Diary"
            apology = "Diary Empty. No WordCloud Available. Showing Default Cloud"

        return render_template("index.html", name=userid, text_db=text_string, year=year, apology=apology) 


    if request.method == "POST":
        
        month = request.form.get('month')
        year = request.form.get('year')

        if int(month) == 0:
            try:
                text_db = db.execute("SELECT mood, text FROM userdata WHERE user_id=? AND year=?;",session['user_id'],year)
            except:
                text_db = "No text found from POST"
        else:
            try:
                text_db = db.execute("SELECT mood, text FROM userdata WHERE user_id=? AND month=? AND year=?;",session['user_id'],month,year)
            except:
                text_db = "No text found from POST"

        text_string = ''
        for entry in text_db:
            for value in entry.values():
                if value and value is not None:
                    # Convert the value to string and remove all punctuations
                    text_string += re.sub(r'[^\w\s]', '', str(value)) + ' '

        if len(text_string) == 0:
            text_string = "Welcome to your WordCloud Diary"
            apology = "Diary Empty. No WordCloud Available. Showing Default Cloud"
        
        return render_template("index.html", name=userid, text_db=text_string, month=calendar.month_name[int(month)], year=year, apology=apology) 

@app.route("/quickentry", methods=["POST"])
@login_required
def quickentry():
    if request.method == "POST":
        entry = request.form.get('entry')
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        if entry:
            db.execute("INSERT INTO userdata (text, user_id, day, month, year) VALUES (?);", (entry, session["user_id"], day, month, year))
        else:
            return redirect('/diary')

    return redirect('/')

#######################
#     DIARY
#######################
@app.route("/diary", methods=["GET", "POST"])
@login_required
def diary():
    """Page to input your thoughts"""
    userid = db.execute("SELECT name FROM users WHERE id = ?;", session['user_id'])[0]['name']

    if request.method == "POST":
        entry = request.form.get('entry')
        mood = " ".join(request.form.getlist('mood'))

        if not entry and not mood:
            return render_template("diary.html", name=userid, apology="No Diary or Mood entry submitted. Try again!")

        try:
            date = datetime.strptime(request.form.get('date'), "%Y-%m-%d").date()
        except:
            date = datetime.now()

        day = date.day
        month = date.month
        year = date.year

        date_db = db.execute("SELECT * FROM userdata WHERE day = ? AND month = ? AND year = ?;", day, month, year)

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
        return redirect("/")

    return render_template("diary.html", name=userid)

#########################
#       SETTINGS
#########################
@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Page to change settings"""
    
    name = db.execute("SELECT name FROM users WHERE id = ?;", session['user_id'])[0]['name']
    username = db.execute("SELECT username FROM users WHERE id = ?;", session['user_id'])[0]['username']
    return render_template("settings.html", name=name, username=username)

@app.route("/change_name", methods=["GET", "POST"])
@login_required
def change_name():
    """Page to change name"""
    
    name = db.execute("SELECT name FROM users WHERE id = ?;", session['user_id'])[0]['name']

    if request.method == "POST":
        name = request.form.get("display_name")
        if not name:
            apology = "No name entered. Try again!"
            return render_template("change_name.html", apology=apology)
        else:
            db.execute("UPDATE users SET name = ? WHERE id = ?;", name, session['user_id'])
            return redirect("/settings")
    
    return render_template("change_name.html", name=name)

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Page to change password"""
    
    password_hash = db.execute("SELECT hash FROM users WHERE id = ?", session['user_id'])[0]['hash']
    
    if request.method == "POST":
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation= request.form.get("confirmation")

        check = check_password_hash(password_hash, old_password)
        
        if not check:
            apology = "Current Password Incorrect. Try Again!"
            return render_template("change_password.html", apology=apology)
        else:
            if new_password != confirmation:
                apology = "Passwords to not match"
                return render_template("change_password.html", apology=apology)
            else:
                db.execute("UPDATE users SET hash = ? WHERE id = ?;", generate_password_hash(new_password), session['user_id'])
                return redirect("/settings")
        
    return render_template("change_password.html")

    


########################
#          VIEW
########################
@app.route("/view", methods=["GET", "POST"])
@login_required
def view():
    """Page see your previous diary entries"""
    userid = db.execute("SELECT name FROM users WHERE id = ?;", session['user_id'])[0]['name']
    apology = ""

    if request.method == "GET":
        date = datetime.now()
        year = date.year
        month = date.month
        day = date.day

        try:
            text_db = db.execute("SELECT day, month, year, mood, text FROM userdata WHERE user_id=? AND day=? AND month=? AND year=?;",session['user_id'],day, month, year)
        except:
            text_db = "No entries found"
        
        if len(text_db) == 0:
            apology = "No entries found"

        # print(text_db)
        return render_template("view.html", name=userid, text_db=text_db, day=day, month=calendar.month_abbr[int(month)], year=year, apology=apology) 


    if request.method == "POST":
        month = request.form.get('month')
        year = request.form.get('year')
        month = request.form.get('month')
        day = request.form.get('day')

        # print(day,month,year)

        if int(month) == 0 and not day:
            apology = "No day or month selected. Showing diary of " + year
            text_db = db.execute("SELECT day, month, year, mood, text FROM userdata WHERE user_id=? AND year=? ORDER BY year ASC, month ASC, day ASC;",session['user_id'], year)
        elif day and int(month) == 0:
            month = datetime.now().month
            apology = "No month selected. Using Current month"
            text_db = db.execute("SELECT day, month, year, mood, text FROM userdata WHERE user_id=? AND day=? AND month=? AND year=? ORDER BY year ASC, month ASC, day ASC;",session['user_id'],day , month, year)
        elif not day:
            text_db = db.execute("SELECT day, month, year, mood, text FROM userdata WHERE user_id=? AND month=? AND year=? ORDER BY year ASC, month ASC, day ASC;",session['user_id'], month, year)
        else:
            text_db = db.execute("SELECT day, month, year, mood, text FROM userdata WHERE user_id=? AND day=? AND month=? AND year=? ORDER BY year ASC, month ASC, day ASC;",session['user_id'],day, month, year)


        if len(text_db) == 0:
            apology = "No entries found"
            
        return render_template("view.html", name=userid, text_db=text_db, day=day, month=calendar.month_abbr[int(month)], year=year, apology=apology) 

#########################
#     ABOUT
#########################
@app.route("/about")
def about():
    """About Page"""
    return render_template("/about.html")




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
            apology = "No username entered"
            return render_template("login.html", apology=apology)

        # Ensure password was submitted
        elif not request.form.get("password"):
            apology = "No password entered"
            return render_template("login.html", apology=apology)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            apology = "Incorrect password. Try again!"
            return render_template("login.html", apology=apology)

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
        name = request.form.get("display_name")
        confirm = request.form.get("confirmation")

        if not username:
            apology = "No username entered"
            return render_template("register.html", apology=apology)
        if not name:
            apology = "No name entered"
            return render_template("register.html", apology=apology)
        elif not password:
            apology = "No password entered"
            return render_template("register.html", apology=apology)
        elif not confirm:
            apology = "No password confimation entered"
            return render_template("register.html", apology=apology)
        elif password != confirm:
            apology = "Passwords to not match"
            return render_template("register.html", apology=apology)

        # Check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        count = len(rows)

        if count != 0:
            apology = "User already exists. Try a different username"
            return render_template("register.html", apology=apology)

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

