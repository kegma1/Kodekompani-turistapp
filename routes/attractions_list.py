from __main__ import app
from flask import render_template, session
from db_utils import Attraction, User, db_session
from libs.helpers import get_user_age

@app.route("/attractions/list", methods = ["GET", "POST"])
def attractions_list():
    try: 
        user = db_session.query(User).filter_by(username=session["user"]).first()
        age = get_user_age(user)
        attractions = db_session.query(Attraction).filter(Attraction.age_recommendation <= age).all()
    except:
        attractions = db_session.query(Attraction).filter(Attraction.age_recommendation == 0).all()
    
    return render_template("view_attractions.html", 
                           attractions = attractions)