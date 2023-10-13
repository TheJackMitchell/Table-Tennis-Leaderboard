# Import nessecary programs

from flask import Flask
from flask import render_template
from flask import request
import csv
import os
from pandas import *

# Open file#
cwd = os.getcwd()

with open(os.path.join(cwd, "leaderboard.csv")) as file:
    data = {}
    users = []
    data = csv.DictReader(file)
    print(data)
    for col in data:
        users.append(col["Name"])

# render page#
app = Flask(__name__, template_folder="template")


@app.route("/", methods=["GET"])
def index():
    global users
    return render_template("index.html", title="Leaderboard", users=users)


# update leaderboard#
@app.route("/match", methods=["GET", "POST"])
def match():
    """function to input a  match result, with validation to ensure only valid entries are made"""
    global users
    valid = False

    X = request.form.get("Winner")
    Y = request.form.get("Loser")

    if X not in users:
        msg = "Winner not in list"
    elif Y not in users:
        msg = "Loser not in list"
    elif X == Y:
        msg = "You can't lose against yourself"
    else:
        valid = True
        change = users.index(X) - users.index(Y)

    if valid == True:
        if users.index(X) > users.index(Y) and change <= 5:
            Wpos = users.index(Y)
            users.remove(X)
            users.insert(Wpos, X)
            msg = "Ranks adjusted"
            with open(os.path.join(cwd, "leaderboard.csv"), "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Name"])
                for x in users:
                    writer.writerow([x])
        elif users.index(X) < users.index(Y):
            msg = "Ranks unchanged because the loser is lower"
        else:
            msg = "Ranks unchanged as difference is over 5"
    return render_template("index.html", title="Match", users=users, MatchMsg=msg)


# add player#
@app.route("/add", methods=["POST"])
def add():
    """function to add a new player to the list, robust against special characters and validated to ensure double entries can't be made"""
    global users
    print(request.form)

    Nuser = request.form["AddPlayer"]
    if Nuser not in users:
        users.insert(len(users) + 1, Nuser)
        msg = "Player added"
    else:
        msg = "Player already on Leaderboard"

    with open(os.path.join(cwd, "leaderboard.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name"])
        for x in users:
            writer.writerow([x])
    return render_template("index.html", title="Add", users=users, AddMsg=msg)


# remove player#
@app.route("/remove", methods=["POST"])
def remove():
    
    """Function to remove players from the database, validated to ensure only people who are in the list can be removed"""
    global users
    print(request.form)

    Ruser = request.form["RemovePlayer"]
    if Ruser in users:
        users.remove(Ruser)
        msg = "Player Removed"
        with open(os.path.join(cwd, "leaderboard.csv"), "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name"])
            for x in users:
                writer.writerow([x])
    else:
        msg = "Player not on Leaderboard"

    return render_template("index.html", title="Remove", users=users, RemoveMsg=msg)

app.run(host="0.0.0.0", port=81)