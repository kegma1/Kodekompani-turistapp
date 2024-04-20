from __main__ import app
from flask import render_template, session
from db_utils import db_session, User, Attraction
from libs.helpers import get_user_status, get_user_age

@app.route("/", methods = ["GET"])
def index():
    pfp = None
    bio = None
    is_logged_in = False
    username = ""
    fullname = ""
    attractions = []
    xp = 0; user_status = "Newbie in city"

    top_5_achievements = None
    
    # fetch attractions for all visitors
    attractions = db_session.query(Attraction).filter(Attraction.age_recommendation <= 0).all()

    if "is_logged_in" in session and session["is_logged_in"]:
        data = db_session.query(User).filter_by(username=session["user"]).first()
        bio = data.bio
        
        user_status = get_user_status(data)

        if data.profile_pic:
            pfp = data.profile_pic

        is_logged_in = True
        username = session["user"]
        fullname = data.full_name

        # Finding top 5 achievements
        if data.achievements is not []:
            top_5_achievements = sorted(data.achievements, key=lambda x: x.xp_reward, reverse=True)[:5]
            
        age = get_user_age(data)

        attractions = db_session.query(Attraction).filter(Attraction.age_recommendation <= age).all()

    return render_template("index.html", 
                           title = "Home page", 
                           pfp = pfp, 
                           bio = bio or None, 
                           is_logged_in = is_logged_in, 
                           username = username, 
                           xp = xp, 
                           user_status = user_status,
                           fullname = fullname, 
                           attractions = attractions,
                           t5achievements = top_5_achievements)
