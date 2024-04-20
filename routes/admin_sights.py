from __main__ import app
from flask import render_template, redirect, url_for
from db_utils import Attraction, db_session, func
from libs.helpers import require_admin, require_login

@app.route("/admin_sights/<page>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_sights(page):
    page = int(page)
    # UPDATED BUT LEFT HERE INCASE OF BÜG
    # attractions = []
    
    # for i in range(page*5 - 5, page*5):
    #     attraction = db_session.query(Attraction).filter_by(id = i).first()
        
    #     if attraction != None:
    #         attractions.append(attraction)
            
    # if attractions == [] and db_session.query(func.count(Attraction.id)).scalar() != 0:
    #     return redirect(url_for("admin_sights", page = 1))
    
    if page < 1:
        return redirect(url_for("admin_sights", page = 1))
    
    attractions = db_session.query(Attraction).offset((page * 5) - 5).limit(5).all()
    
    if not attractions and page != 1:
        return redirect(url_for("admin_sights", page = 1))
    
    return render_template("admin_sights.html", 
                           attractions = attractions,
                           page = page)