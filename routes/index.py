from __main__ import app
from flask import render_template, session
from db_utils import db_session, User
from io import BytesIO
from PIL import Image

@app.route("/", methods = ["GET"])
def index():
    pfp = None
    is_logged_in = False
    username = ""

    if "is_logged_in" in session and session["is_logged_in"]:
        pfp_data = db_session.query(User.profile_pic).filter_by(username=session["user"]).first()
        print(pfp_data)
        # pfp = Image.open(BytesIO(pfp_data))
        is_logged_in = True
        username = session["user"]


    return render_template("index.html", title="Home page", pfp=pfp, is_logged_in=is_logged_in, username=username)