from __main__ import app
from flask import render_template
from db_utils import Attraction, db_session
from libs.helpers import require_admin, require_login

@app.route("/admin_sights", methods = ["GET", "POST"])
@require_login
@require_admin
def admin_sights():
    return render_template("admin_sights.html", 
                           attractions = db_session.query(Attraction).all())