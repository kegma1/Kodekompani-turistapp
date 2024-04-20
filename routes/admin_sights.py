from __main__ import app
from flask import render_template, redirect, url_for
from db_utils import Attraction, db_session, func
from libs.helpers import require_admin, require_login, paging

@app.route("/admin_sights/<int:page>", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_sights(page):
    data = paging(page, 5, Attraction)
    
    if not data:
        return redirect(url_for("admin_sights", page = 1))
    
    return render_template("admin_sights.html", 
                           attractions = data,
                           page = page)