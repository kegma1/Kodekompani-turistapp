from __main__ import app

from flask import render_template, redirect, url_for, flash
from db_utils import Achievement, db_session, func  
from libs.helpers import require_admin, require_login, paging

@app.route("/admin_achievements/<int:page>", methods=["GET", "POST"])
@require_login
@require_admin
def admin_achievements(page):
    data = paging(page, 5, Achievement)   

    if not data:
        return redirect(url_for("admin_achievements", page = 1))
     
    return render_template("admin_achievements.html", 
                           achievements= data,
                           page=page)

    


@app.route("/toggle_achievement_status/<int:id>", methods=["POST"])
@require_login
@require_admin
def toggle_achievement_status(id):
    achievement = db_session.query(Achievement).filter_by(id=id).first()
    if achievement:
        achievement.is_deleted = not achievement.is_deleted
        db_session.commit()
        flash("Achievement status updated successfully.", "success")
    else:
        flash("Achievement not found.", "error")

    return redirect(url_for('admin_achievements', page=1))