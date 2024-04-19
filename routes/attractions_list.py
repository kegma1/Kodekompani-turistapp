from __main__ import app
from flask import render_template, session, redirect, url_for
from db_utils import Attraction, User, db_session
from libs.helpers import get_user_age, require_login

@require_login
@app.route("/attractions/list", methods = ["GET", "POST"])
def attractions_list(): 
    user = db_session.query(User).filter_by(username=session["user"]).first()
    age = get_user_age(user)
    attractions = db_session.query(Attraction).filter(Attraction.age_recommendation <= age).all()
    
    return render_template("view_attractions.html", 
                           attractions = attractions)