from __main__ import app
from flask import render_template, session
from db_utils import db_session, User
from base64 import b64encode

@app.route("/", methods = ["GET"])
def index():
    pfp = None
    bio = None
    is_logged_in = False
    username = ""
    fullname = ""
    xp = 0; user_status = "Newbie in city"

    if "is_logged_in" in session and session["is_logged_in"]:
        data = db_session.query(User).filter_by(username=session["user"]).first()
        bio = data.bio
        
        xp = data.xp_collected
        xp = 0 if xp == None else xp
        if xp < 10: user_status = "Newbie in city"
        elif xp < 50: user_status = "Tourist"
        elif xp < 100: user_status = "Svarta bjorn"
        else: user_status = "Rallar"

        if data.profile_pic:
            pfp = data.profile_pic

        is_logged_in = True
        username = session["user"]
        fullname = data.full_name

    return render_template("index.html", title="Home page", pfp=pfp, bio = bio or None, 
                           is_logged_in=is_logged_in, username=username, xp=xp, user_status=user_status,
                           fullname = fullname) 