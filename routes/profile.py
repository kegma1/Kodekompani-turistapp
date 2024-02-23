from __main__ import app, redirect, render_template, url_for
from utils import Friend, User, UserAttraction, UserAchievement, db_session

@app.route("/profile", methods = ["GET", "POST"])
def profile():
    pass