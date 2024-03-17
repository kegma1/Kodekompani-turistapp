from __main__ import app
from flask import render_template
from db_utils import Attraction, db_session

@app.route("/attractions/list", methods = ["GET", "POST"])
def attractions_list():
    return render_template("view_attractions.html", 
                           attractions = db_session.query(Attraction).all())