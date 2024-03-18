from __main__ import app
from flask import render_template, redirect, url_for
from db_utils import Attraction, db_session
from libs.helpers import require_admin, require_login

@app.route("/admin_sights/<page>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_sights(page):
    page = int(page)
    attractions = []
    for i in range(page*5 - 5, page*5):
        attraction = db_session.query(Attraction).filter_by(id = i).first()
        
        if attraction != None:
            attractions.append(attraction)
            
    if attractions == []:
        return redirect(url_for("admin_sights", page = 1))
    
    return render_template("admin_sights.html", 
                           attractions = attractions,
                           page = page)