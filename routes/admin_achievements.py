from __main__ import app

from flask import render_template, redirect, url_for, flash
from db_utils import Achievement, db_session  
from libs.helpers import require_admin, require_login, paging, require_local_admin

@app.route("/admin_achievements/<int:page>", methods=["GET", "POST"])
@app.route("/admin_achievements/<int:page>/<attraction_id>", methods=["GET", "POST"])
@require_login
@require_local_admin
def admin_achievements(page, attraction_id = None):
    data = None

    if attraction_id is not None:
        data = paging(page, 5, query=db_session.query(Achievement).filter_by(attraction_id=attraction_id))   
    else:
        data = paging(page, 5, Achievement)   

    if data is None:
        return redirect(url_for("admin_achievements", page = 1, attraction_id=attraction_id))

     
    return render_template("admin_achievements.html", 
                           achievements= data,
                           attraction_id=attraction_id,
                           page=page)


@app.route("/toggle_achievement_status/<int:id>", methods=["POST"])
@app.route("/toggle_achievement_status/<int:id>/<attraction_id>", methods=["POST"])
@require_login
@require_local_admin
def toggle_achievement_status(id, attraction_id = None):
    achievement = db_session.query(Achievement).filter_by(id=id).first()
    if achievement:
        achievement.is_deleted = not achievement.is_deleted
        db_session.commit()
        flash("Achievement status updated successfully.", "success")
    else:
        flash("Achievement not found.", "error")

    return redirect(url_for('admin_achievements', page=1, attraction_id=attraction_id))