from __main__ import app, redirect, render_template, url_for
from flask import request
from db_utils import Friend, User, UserAttraction, UserAchievement, db_session
from PIL import Image
from io import BytesIO
from base64 import b64encode

@app.route("/admin", methods = ["GET", "POST"]) # Needs more checks for admin privileges in the future
def admin():
    return render_template("admin.html", 
                        friends = db_session.query(Friend).all(), 
                        users = db_session.query(User).all(), 
                        user_attractions = db_session.query(UserAttraction).all(), 
                        user_achievement = db_session.query(UserAchievement).all(),
                        title = "Admin Page")