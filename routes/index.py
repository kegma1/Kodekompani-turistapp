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

    if "is_logged_in" in session and session["is_logged_in"]:
        data = db_session.query(User).filter_by(username=session["user"]).first()
        bio = data.bio

        if data.profile_pic:
            pfp = data.profile_pic

        is_logged_in = True
        username = session["user"]

    return render_template("index.html", title="Home page", pfp=pfp, bio = bio or None, is_logged_in=is_logged_in, username=username)  