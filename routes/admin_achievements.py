from __main__ import app

from flask import render_template, redirect, url_for, flash, request
from db_utils import Achievement, db_session, func  
from libs.helpers import require_admin, require_login

@app.route("/admin_achievements/<int:page>", methods=["GET", "POST"])
@require_login
@require_admin
def admin_achievements(page):
    achievements = []
    
    for i in range(page*5 - 5, page*5):
        achievement = db_session.query(Achievement).filter_by(id=i).first()
        
        if achievement is not None:
            achievements.append(achievement)
            
    if not achievements and db_session.query(func.count(Achievement.id)).scalar() != 0:
        return redirect(url_for("admin_achievements", page=1))
    
    return render_template("admin_achievements.html", 
                           achievements=achievements,
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