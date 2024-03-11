from __main__ import app
from libs.helpers import require_login
from flask import request,  redirect, render_template, url_for, session
from db_utils import Attraction, db_session

@app.route("/view_attractions", methods = ["GET", "POST"])
def view_attractions():
    info = db_session.query(Attraction).all()
    print('results: ', info)
    return render_template("view_attractions.html", title = "test")