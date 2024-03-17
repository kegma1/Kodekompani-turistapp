from __main__ import app
from libs.helpers import require_login
from flask import request,  redirect, render_template, url_for, session
from db_utils import Attraction, db_session

@app.route("/attractions/list", methods = ["GET", "POST"])
def attractions_list():
    return render_template("view_attractions.html", 
                           attractions = db_session.query(Attraction).all())