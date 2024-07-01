import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from timeHelper import get_time
import schedule
import time
import threading
import json
from bs4 import BeautifulSoup
import requests
import datetime
from webScrapper import scrapper 
from dotenv import load_dotenv
from openai import OpenAI
from triviaGenerator import triviaCreator



from helpers import login_required

# Configure Application
app = Flask(__name__, static_url_path='/static')

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///triviaTrials.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        try:
            id = session["user_id"]
        except:
            return redirect("/login")

        tableName = "table" + str(id)

        leaderBoardStats= {}

        classicScoreTodayQuery = "SELECT classicScoreToday FROM {}".format(tableName)
        leaderBoardStats['classicScoreToday']  = (int)(db.execute(classicScoreTodayQuery)[0]["classicScoreToday"])

        classicQuestionsTodayQuery = "SELECT classicQuestionsToday FROM {}".format(tableName)
        leaderBoardStats['classicQuestionsToday']  = (int)(db.execute(classicQuestionsTodayQuery)[0]["classicQuestionsToday"])

        classicScoreAllTimeQuery = "SELECT classicScoreAllTime FROM {}".format(tableName)
        leaderBoardStats['classicScoreAllTime']  = (int)(db.execute(classicScoreAllTimeQuery)[0]["classicScoreAllTime"])

        classicQuestionsAllTimeQuery = "SELECT classicQuestionsAllTime FROM {}".format(tableName)
        leaderBoardStats['classicQuestionsAllTime']  = (int)(db.execute(classicQuestionsAllTimeQuery)[0]["classicQuestionsAllTime"])

        miniScoreTodayQuery = "SELECT miniScoreToday FROM {}".format(tableName)
        leaderBoardStats['miniScoreToday']  = (int)(db.execute(miniScoreTodayQuery)[0]["miniScoreToday"])

        miniQuestionsTodayQuery = "SELECT miniQuestionsToday FROM {}".format(tableName)
        leaderBoardStats['miniQuestionsToday']  = (int)(db.execute(miniQuestionsTodayQuery)[0]["miniQuestionsToday"])

        miniScoreAllTimeQuery = "SELECT miniScoreAllTime FROM {}".format(tableName)
        leaderBoardStats['miniScoreAllTime']  = (int)(db.execute(miniScoreAllTimeQuery)[0]["miniScoreAllTime"])

        miniQuestionsAllTimeQuery = "SELECT miniQuestionsAllTime FROM {}".format(tableName)
        leaderBoardStats['miniQuestionsAllTime']  = (int)(db.execute(miniQuestionsAllTimeQuery)[0]["miniQuestionsAllTime"])

        if session.get("user_id") is None: 
            return redirect("/login")
        elif 'mini' in request.form:
            if leaderBoardStats["miniQuestionsToday"] >= 5:
                return redirect("/leaderboardMiniSummary")
            else:
                return redirect("/mini")
        elif 'classic' in request.form:
            if leaderBoardStats["classicQuestionsToday"] >= 15:
                return redirect("/leaderboardClassicSummary")
            else:
                return redirect("/classic")

    else: 
        today = dateCreator()
        return render_template("index.html", today=today)
    

@app.route("/classic", methods=["GET", "POST"])
@login_required
def classic():

    if request.method == "POST":
        checkDisclaimerData = request.json
        delete_disclaimer = checkDisclaimerData.get('deleteDisclaimer')
        if delete_disclaimer:
            id = session["user_id"]
            tableName = "table" + str(id)

            deleteDisclaimer = "UPDATE {} SET clearedDisclaimerClassic = 1".format(tableName)
            db.execute(deleteDisclaimer)

        return jsonify({'status': 'success', 'deleteDisclaimer': delete_disclaimer})


    else:
        id = session["user_id"]
        tableName = "table" + str(id)

        deleteDisclaimer = "SELECT clearedDisclaimerClassic FROM {}".format(tableName)
        noDisclaimer = (int)(db.execute(deleteDisclaimer)[0]["clearedDisclaimerClassic"])
        questionDict = {"correct": 0, "questions": 0}
        return render_template("classicLoadingPage.html", questionDict=questionDict, noDisclaimer=noDisclaimer) 
    

@app.route("/mini", methods=["GET", "POST"])
@login_required
def mini():

    if request.method == "POST":
        checkDisclaimerData = request.json
        delete_disclaimer = checkDisclaimerData.get('deleteDisclaimer')
        if delete_disclaimer:
            id = session["user_id"]
            tableName = "table" + str(id)

            deleteDisclaimer = "UPDATE {} SET clearedDisclaimerMini = 1".format(tableName)
            db.execute(deleteDisclaimer)

        return jsonify({'status': 'success', 'deleteDisclaimer': delete_disclaimer})


    else:
        id = session["user_id"]
        tableName = "table" + str(id)

        deleteDisclaimer = "SELECT clearedDisclaimerMini FROM {}".format(tableName)
        noDisclaimer = (int)(db.execute(deleteDisclaimer)[0]["clearedDisclaimerMini"])
        questionDict = {"correct": 0, "questions": 0}
        return render_template("miniLoadingPage.html", questionDict=questionDict, noDisclaimer=noDisclaimer) 
    

@app.route("/miniStart", methods=["GET"])
@login_required
def miniStart():
    id = session["user_id"]
    questions = getTodaysQuestions2()

    
    tableName = "table" + str(id)
    leaderBoardStats= {}

    classicScoreTodayQuery = "SELECT classicScoreToday FROM {}".format(tableName)
    leaderBoardStats['classicScoreToday']  = (int)(db.execute(classicScoreTodayQuery)[0]["classicScoreToday"])

    classicQuestionsTodayQuery = "SELECT classicQuestionsToday FROM {}".format(tableName)
    leaderBoardStats['classicQuestionsToday']  = (int)(db.execute(classicQuestionsTodayQuery)[0]["classicQuestionsToday"])

    classicScoreAllTimeQuery = "SELECT classicScoreAllTime FROM {}".format(tableName)
    leaderBoardStats['classicScoreAllTime']  = (int)(db.execute(classicScoreAllTimeQuery)[0]["classicScoreAllTime"])

    classicQuestionsAllTimeQuery = "SELECT classicQuestionsAllTime FROM {}".format(tableName)
    leaderBoardStats['classicQuestionsAllTime']  = (int)(db.execute(classicQuestionsAllTimeQuery)[0]["classicQuestionsAllTime"])

    miniScoreTodayQuery = "SELECT miniScoreToday FROM {}".format(tableName)
    leaderBoardStats['miniScoreToday']  = (int)(db.execute(miniScoreTodayQuery)[0]["miniScoreToday"])

    miniQuestionsTodayQuery = "SELECT miniQuestionsToday FROM {}".format(tableName)
    leaderBoardStats['miniQuestionsToday']  = (int)(db.execute(miniQuestionsTodayQuery)[0]["miniQuestionsToday"])

    miniScoreAllTimeQuery = "SELECT miniScoreAllTime FROM {}".format(tableName)
    leaderBoardStats['miniScoreAllTime']  = (int)(db.execute(miniScoreAllTimeQuery)[0]["miniScoreAllTime"])

    miniQuestionsAllTimeQuery = "SELECT miniQuestionsAllTime FROM {}".format(tableName)
    leaderBoardStats['miniQuestionsAllTime']  = (int)(db.execute(miniQuestionsAllTimeQuery)[0]["miniQuestionsAllTime"])

    print(leaderBoardStats["miniQuestionsToday"])
    if leaderBoardStats["miniQuestionsToday"] >= 5:
            return redirect("/")

    return render_template("question1Mini.html", questions=questions, leaderBoardStats=leaderBoardStats)
    

@app.route("/classicStart", methods=["GET", "POST"])
@login_required
def classicStart():
        id = session["user_id"]
        questions = getTodaysQuestions2()

        
        tableName = "table" + str(id)
        leaderBoardStats= {}

        classicScoreTodayQuery = "SELECT classicScoreToday FROM {}".format(tableName)
        leaderBoardStats['classicScoreToday']  = (int)(db.execute(classicScoreTodayQuery)[0]["classicScoreToday"])

        classicQuestionsTodayQuery = "SELECT classicQuestionsToday FROM {}".format(tableName)
        leaderBoardStats['classicQuestionsToday']  = (int)(db.execute(classicQuestionsTodayQuery)[0]["classicQuestionsToday"])

        classicScoreAllTimeQuery = "SELECT classicScoreAllTime FROM {}".format(tableName)
        leaderBoardStats['classicScoreAllTime']  = (int)(db.execute(classicScoreAllTimeQuery)[0]["classicScoreAllTime"])

        classicQuestionsAllTimeQuery = "SELECT classicQuestionsAllTime FROM {}".format(tableName)
        leaderBoardStats['classicQuestionsAllTime']  = (int)(db.execute(classicQuestionsAllTimeQuery)[0]["classicQuestionsAllTime"])

        miniScoreTodayQuery = "SELECT miniScoreToday FROM {}".format(tableName)
        leaderBoardStats['miniScoreToday']  = (int)(db.execute(miniScoreTodayQuery)[0]["miniScoreToday"])

        miniQuestionsTodayQuery = "SELECT miniQuestionsToday FROM {}".format(tableName)
        leaderBoardStats['miniQuestionsToday']  = (int)(db.execute(miniQuestionsTodayQuery)[0]["miniQuestionsToday"])

        miniScoreAllTimeQuery = "SELECT miniScoreAllTime FROM {}".format(tableName)
        leaderBoardStats['miniScoreAllTime']  = (int)(db.execute(miniScoreAllTimeQuery)[0]["miniScoreAllTime"])

        miniQuestionsAllTimeQuery = "SELECT miniQuestionsAllTime FROM {}".format(tableName)
        leaderBoardStats['miniQuestionsAllTime']  = (int)(db.execute(miniQuestionsAllTimeQuery)[0]["miniQuestionsAllTime"])

        if leaderBoardStats["classicQuestionsToday"] >= 15:
            return redirect("/")

        return render_template("question1Classic.html", questions=questions, leaderBoardStats=leaderBoardStats)

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
        today = dateCreator()
        classicWinnersToday = db.execute("SELECT playerName, classicPercentToday FROM leaderboard ORDER BY classicPercentToday DESC LIMIT 5")
        classicWinnersAllTime = db.execute("SELECT playerName, classicPercentAllTime FROM leaderboard ORDER BY classicPercentAllTime DESC LIMIT 5")
        miniWinnersToday = db.execute("SELECT playerName, miniPercentToday FROM leaderboard ORDER BY miniPercentToday DESC LIMIT 5")
        miniWinnersAllTime = db.execute("SELECT playerName, miniPercentAllTime FROM leaderboard ORDER BY miniPercentAllTime DESC LIMIT 5")

        for x in range(1, len(classicWinnersToday) + 1):
            classicWinnersToday[x - 1]["rank"] = x

        for x in range(1, len(classicWinnersAllTime) + 1):
            classicWinnersAllTime[x - 1]["rank"] = x

        for x in range(1, len(miniWinnersToday) + 1):
            miniWinnersToday[x - 1]["rank"] = x

        for x in range(1, len(miniWinnersAllTime) + 1):
            miniWinnersAllTime[x - 1]["rank"] = x
        
        return render_template("leaderboard.html", today=today, classicWinnersToday=classicWinnersToday, classicWinnersAllTime=classicWinnersAllTime, miniWinnersToday=miniWinnersToday, miniWinnersAllTime=miniWinnersAllTime)

@app.route("/leaderboardClassicSummary")
@login_required
def leaderboardClassicSummary(): 
    id = session["user_id"]
    tableName = "table" + str(id)

    db.execute("UPDATE leaderboard SET classicQuestionsToday = 15")
    classicInCaseRaceConditionUpdate = "UPDATE {} SET classicQuestionsToday = 15".format(tableName)
    db.execute(classicInCaseRaceConditionUpdate)

    leaderBoardStats= {}

    classicScoreTodayQuery = "SELECT classicScoreToday FROM {}".format(tableName)
    leaderBoardStats['classicScoreToday']  = (int)(db.execute(classicScoreTodayQuery)[0]["classicScoreToday"])

    classicQuestionsTodayQuery = "SELECT classicQuestionsToday FROM {}".format(tableName)
    leaderBoardStats['classicQuestionsToday']  = (int)(db.execute(classicQuestionsTodayQuery)[0]["classicQuestionsToday"])

    classicScoreAllTimeQuery = "SELECT classicScoreAllTime FROM {}".format(tableName)
    leaderBoardStats['classicScoreAllTime']  = (int)(db.execute(classicScoreAllTimeQuery)[0]["classicScoreAllTime"])

    classicQuestionsAllTimeQuery = "SELECT classicQuestionsAllTime FROM {}".format(tableName)
    leaderBoardStats['classicQuestionsAllTime']  = (int)(db.execute(classicQuestionsAllTimeQuery)[0]["classicQuestionsAllTime"])

    miniScoreTodayQuery = "SELECT miniScoreToday FROM {}".format(tableName)
    leaderBoardStats['miniScoreToday']  = (int)(db.execute(miniScoreTodayQuery)[0]["miniScoreToday"])

    miniQuestionsTodayQuery = "SELECT miniQuestionsToday FROM {}".format(tableName)
    leaderBoardStats['miniQuestionsToday']  = (int)(db.execute(miniQuestionsTodayQuery)[0]["miniQuestionsToday"])

    miniScoreAllTimeQuery = "SELECT miniScoreAllTime FROM {}".format(tableName)
    leaderBoardStats['miniScoreAllTime']  = (int)(db.execute(miniScoreAllTimeQuery)[0]["miniScoreAllTime"])

    miniQuestionsAllTimeQuery = "SELECT miniQuestionsAllTime FROM {}".format(tableName)
    leaderBoardStats['miniQuestionsAllTime']  = (int)(db.execute(miniQuestionsAllTimeQuery)[0]["miniQuestionsAllTime"])

    today = dateCreator()
    return render_template("classicSummary.html", today=today, leaderBoardStats=leaderBoardStats)

@app.route("/leaderboardMiniSummary")
@login_required
def leaderboardMiniSummary(): 
    id = session["user_id"]
    tableName = "table" + str(id)

    db.execute("UPDATE leaderboard SET miniQuestionsToday = 5")
    miniInCaseRaceConditionUpdate = "UPDATE {} SET miniQuestionsToday = 5".format(tableName)
    db.execute(miniInCaseRaceConditionUpdate)

    leaderBoardStats= {}

    classicScoreTodayQuery = "SELECT classicScoreToday FROM {}".format(tableName)
    leaderBoardStats['classicScoreToday']  = (int)(db.execute(classicScoreTodayQuery)[0]["classicScoreToday"])

    classicQuestionsTodayQuery = "SELECT classicQuestionsToday FROM {}".format(tableName)
    leaderBoardStats['classicQuestionsToday']  = (int)(db.execute(classicQuestionsTodayQuery)[0]["classicQuestionsToday"])

    classicScoreAllTimeQuery = "SELECT classicScoreAllTime FROM {}".format(tableName)
    leaderBoardStats['classicScoreAllTime']  = (int)(db.execute(classicScoreAllTimeQuery)[0]["classicScoreAllTime"])

    classicQuestionsAllTimeQuery = "SELECT classicQuestionsAllTime FROM {}".format(tableName)
    leaderBoardStats['classicQuestionsAllTime']  = (int)(db.execute(classicQuestionsAllTimeQuery)[0]["classicQuestionsAllTime"])

    miniScoreTodayQuery = "SELECT miniScoreToday FROM {}".format(tableName)
    leaderBoardStats['miniScoreToday']  = (int)(db.execute(miniScoreTodayQuery)[0]["miniScoreToday"])

    miniQuestionsTodayQuery = "SELECT miniQuestionsToday FROM {}".format(tableName)
    leaderBoardStats['miniQuestionsToday']  = (int)(db.execute(miniQuestionsTodayQuery)[0]["miniQuestionsToday"])

    miniScoreAllTimeQuery = "SELECT miniScoreAllTime FROM {}".format(tableName)
    leaderBoardStats['miniScoreAllTime']  = (int)(db.execute(miniScoreAllTimeQuery)[0]["miniScoreAllTime"])

    miniQuestionsAllTimeQuery = "SELECT miniQuestionsAllTime FROM {}".format(tableName)
    leaderBoardStats['miniQuestionsAllTime']  = (int)(db.execute(miniQuestionsAllTimeQuery)[0]["miniQuestionsAllTime"])

    today = dateCreator()
    return render_template("miniSummary.html", today=today, leaderBoardStats=leaderBoardStats)

@app.route("/questionSubmitClassic", methods = ["POST"])
@login_required
def questionSubmitClassic():

    submittedDictionary = request.get_json()
    id = session["user_id"]
    db.execute("UPDATE leaderboard SET classicScoreToday = ?, classicQuestionsToday = ? WHERE id = ? ", submittedDictionary["classicScoreToday"], submittedDictionary["classicQuestionsToday"], id)
    tableName = "table" + str(id)
    usersTableQuery = "UPDATE {} SET classicScoreToday = ?, classicQuestionsToday = ?" .format(tableName)
    db.execute(usersTableQuery, submittedDictionary["classicScoreToday"], submittedDictionary["classicQuestionsToday"])

    if submittedDictionary["isQuestionCorrect"]:
        usersTableQuery2 = "UPDATE {} SET classicScoreAllTime = classicScoreAllTime + 1, classicQuestionsAllTime = classicQuestionsAllTime + 1" .format(tableName)
        db.execute("UPDATE leaderboard SET classicScoreAllTime = classicScoreAllTime + 1, classicQuestionsAllTime = classicQuestionsAllTime + 1 WHERE id = ? ", id)
        db.execute(usersTableQuery2)
    else:
        usersTableQuery2 = "UPDATE {} SET classicQuestionsAllTime = classicQuestionsAllTime + 1" .format(tableName)
        db.execute("UPDATE leaderboard SET classicQuestionsAllTime = classicQuestionsAllTime + 1 WHERE id = ?", id)
        db.execute(usersTableQuery2)

    return '', 204 

@app.route("/questionSubmitMini", methods = ["POST"])
@login_required
def miniSubmitClassic():

    submittedDictionary = request.get_json()
    id = session["user_id"]
    db.execute("UPDATE leaderboard SET miniScoreToday = ?, miniQuestionsToday = ? WHERE id = ? ", submittedDictionary["miniScoreToday"], submittedDictionary["miniQuestionsToday"], id)

    tableName = "table" + str(id)
    usersTableQuery = "UPDATE {} SET miniScoreToday = ?, miniQuestionsToday = ?" .format(tableName)
    db.execute(usersTableQuery, submittedDictionary["miniScoreToday"], submittedDictionary["miniQuestionsToday"])

    if submittedDictionary["isQuestionCorrect"]:
        usersTableQuery2 = "UPDATE {} SET miniScoreAllTime = miniScoreAllTime + 1, miniQuestionsAllTime = miniQuestionsAllTime + 1" .format(tableName)
        db.execute("UPDATE leaderboard SET miniScoreAllTime = miniScoreAllTime + 1, miniQuestionsAllTime = miniQuestionsAllTime + 1 WHERE id = ? ", id)

        db.execute(usersTableQuery2)
        
    else:
        usersTableQuery2 = "UPDATE {} SET miniQuestionsAllTime = miniQuestionsAllTime + 1" .format(tableName)
        db.execute(usersTableQuery2)
        db.execute("UPDATE leaderboard SET miniQuestionsAllTime = miniQuestionsAllTime + 1 WHERE id = ?", id)

    return '', 204 

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        email = request.form.get("email") #gets email from form 
        
        if not email: 
            flash("Error Please Enter Your Email")
            return render_template("register.html")
            
        troublesomeCharacters = ["&",'"', "'", "[", "]", "%", ";", "_", "-", "/", "\\", "*"]
        for character in email:
            if character in troublesomeCharacters:
                flash(f"Email cannot include {character}") 
                return render_template("register.html")

        emailCheck = db.execute("SELECT id FROM users WHERE email = ?", email)
        
        if emailCheck:
            flash("Error: User Already Exists")
            return render_template("register.html")
        

        name = request.form.get("name") #gets email from form 
        
        if not name: 
            flash("Error Please Enter Your Name")
            return render_template("register.html")
            
        for character in name:
            if character in troublesomeCharacters:
                flash(f"Email cannot include {character}") 
                return render_template("register.html")
            
        password = request.form.get("password")

        if not password:
            flash("Error: Please Enter Your Password")
            return render_template("register.html")
        
        for character in password:
            if character in troublesomeCharacters:
                flash(f"Password cannot include {character}") 
                return render_template("register.html")

            
        confirm = request.form.get("confirm")

        if not confirm:
            flash("Error: Please Confirm Your Password")
            return render_template("register.html")
        
        for character in confirm:
            if character in troublesomeCharacters:
                flash(f"Confirm cannot include {character}") 
                return render_template("register.html")
            
        if password != confirm:
            flash("Error: Passwords Do Not Match")
            return render_template("register.html")
        
        hashedPass = generate_password_hash(password, method="pbkdf2", salt_length=16)
        db.execute("INSERT INTO users (email, hash) VALUES(?, ?)", email, hashedPass)

        rows = db.execute("SELECT * FROM users WHERE email = ?", email)
        session["user_id"] = rows[0]["id"]

        id = session["user_id"]
        tableName = "table" + str(id)

        createTableQuery = "CREATE TABLE {} (didMini INTEGER, didClassic INTEGER, miniScoreToday INTEGER, miniQuestionsToday INTEGER,  classicScoreToday INTEGER, classicQuestionsToday INTEGER, miniScoreAllTime INTEGER,  miniQuestionsAllTime INTEGER, classicScoreAllTime INTEGER, classicQuestionsAllTime INTEGER,  dateOfCreation CURRENT_TIMESTAMP,   clearedDisclaimerClassic INTEGER,    clearedDisclaimerMini INTEGER,    miniScorePercentageToday FLOAT GENERATED ALWAYS AS (CASE WHEN miniQuestionsToday > 0 THEN (miniScoreToday * 1.0 / miniQuestionsToday) ELSE 0.0 END),    classicScorePercentageToday FLOAT GENERATED ALWAYS AS (CASE WHEN classicQuestionsToday > 0.0 THEN (classicScoreToday * 1.0 / classicQuestionsToday) ELSE 0.0 END),miniScorePercentageAllTime FLOAT GENERATED ALWAYS AS (CASE WHEN miniQuestionsAllTime > 0 THEN (miniScoreAllTime * 1.0 / miniQuestionsAllTime) ELSE 0.0 END), classicScorePercentageAllTime FLOAT GENERATED ALWAYS AS (CASE WHEN classicQuestionsAllTime > 0 THEN (classicScoreAllTime * 1.0 / classicQuestionsAllTime) ELSE 0.0 END));" .format(tableName)
        db.execute(createTableQuery)

        insertTableQuery = "INSERT INTO {} ( didMini, didClassic, miniScoreToday, miniQuestionsToday, classicScoreToday, classicQuestionsToday, miniScoreAllTime, miniQuestionsAllTime, classicScoreAllTime, classicQuestionsAllTime, clearedDisclaimerClassic, clearedDisclaimerMini, dateOfCreation) VALUES (0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  0, 0, CURRENT_TIMESTAMP)".format(tableName)        
        db.execute(insertTableQuery)

        db.execute("INSERT INTO leaderboard (id, playerName, miniScoreToday, miniQuestionsToday, miniScoreAllTime, miniQuestionsAllTime, classicScoreToday, classicQuestionsToday, classicScoreAllTime, classicQuestionsAllTime) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", id , name , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0)

        
        
        return redirect("/")
    else: 
        return render_template("register.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("email"):
            flash("Error: Please Enter An Email")
            return render_template("login.html")

        elif not request.form.get("paswrd"):
            flash("Error: Please Enter A Password")
            return render_template("login.html")
        
        rows = db.execute(
            "SELECT * FROM users WHERE email = ?", request.form.get("email")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("paswrd")
        ):
            flash("Error: Invalid Username and/or Password")
            return render_template("login.html")
        
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    else:
        return render_template("login.html")

     

@app.route("/logout", methods=["GET"])
@login_required
def logout():
        session.clear()

        flash("Successfully Logged Out")
        return redirect("/")
    
# Ensure the app runs with debug mode enabled
if __name__ == '__main__':
    app.run(debug=True)

def dateCreator():
    weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    date = {}

    date["weekday"] = weekday_names[datetime.datetime.now().weekday()]
    date["month"] = months[datetime.datetime.now().month - 1] 
    date["day"] = datetime.datetime.now().day
    date["year"] = datetime.datetime.now().year
    
    return date


@app.route('/get_time2')
def get_time2():
    return jsonify({'current_time': datetime.datetime.now().isoformat()})

@app.route('/getUserScores')
@login_required
def get_userScores():
    id = session["user_id"]
    tableName = "table" + str(id)

    leaderBoardStats = {}

    classicScoreTodayQuery = "SELECT classicScoreToday FROM {}".format(tableName)
    leaderBoardStats['classicScoreToday']  = (int)(db.execute(classicScoreTodayQuery)[0]["classicScoreToday"])

    classicQuestionsTodayQuery = "SELECT classicQuestionsToday FROM {}".format(tableName)
    leaderBoardStats['classicQuestionsToday']  = (int)(db.execute(classicQuestionsTodayQuery)[0]["classicQuestionsToday"])

    classicScoreAllTimeQuery = "SELECT classicScoreAllTime FROM {}".format(tableName)
    leaderBoardStats['classicScoreAllTime']  = (int)(db.execute(classicScoreAllTimeQuery)[0]["classicScoreAllTime"])

    classicQuestionsAllTimeQuery = "SELECT classicQuestionsAllTime FROM {}".format(tableName)
    leaderBoardStats['classicQuestionsAllTime']  = (int)(db.execute(classicQuestionsAllTimeQuery)[0]["classicQuestionsAllTime"])

    miniScoreTodayQuery = "SELECT miniScoreToday FROM {}".format(tableName)
    leaderBoardStats['miniScoreToday']  = (int)(db.execute(miniScoreTodayQuery)[0]["miniScoreToday"])

    miniQuestionsTodayQuery = "SELECT miniQuestionsToday FROM {}".format(tableName)
    leaderBoardStats['miniQuestionsToday']  = (int)(db.execute(miniQuestionsTodayQuery)[0]["miniQuestionsToday"])

    miniScoreAllTimeQuery = "SELECT miniScoreAllTime FROM {}".format(tableName)
    leaderBoardStats['miniScoreAllTime']  = (int)(db.execute(miniScoreAllTimeQuery)[0]["miniScoreAllTime"])

    miniQuestionsAllTimeQuery = "SELECT miniQuestionsAllTime FROM {}".format(tableName)
    leaderBoardStats['miniQuestionsAllTime']  = (int)(db.execute(miniQuestionsAllTimeQuery)[0]["miniQuestionsAllTime"])


    return jsonify(leaderBoardStats)

@app.route('/getTodaysQuestions')
def getTodaysQuestions():
    with open('./trivia_questions.json', 'r') as file:
        questions = json.load(file)
    return jsonify(questions)

def getTodaysQuestions2():
    with open('./trivia_questions.json', 'r') as file:
        questions = json.load(file)
    return questions

def task():
    ids = db.execute("SELECT id FROM leaderboard")
    
    for x in range(0, len(ids)):
        tablename = "table" + str(ids[x]["id"])
        queryForReset = "UPDATE {} SET didMini = 0, didClassic = 0, miniScoreToday = 0, miniQuestionsToday = 0, classicQuestionsToday = 0, classicScoreToday = 0".format(tablename)
        db.execute(queryForReset)
    
    db.execute("UPDATE leaderboard SET miniScoreToday = 0, miniQuestionsToday = 0, classicScoreToday = 0, classicQuestionsToday = 0")

    scrapper()
    time.sleep(20)
    triviaCreator()


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

schedule.every().day.at("00:00").do(task)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()