from __main__ import app

from flask import request, redirect, render_template, url_for, flash
from db_utils import Achievement, db_session  
from libs.helpers import require_local_admin, require_login
from form.achievement_form import AchievementForm  
from werkzeug.datastructures import CombinedMultiDict

@app.route("/admin_achievements_edit/<int:id>", methods=["GET", "POST"])
@app.route("/admin_achievements_edit/<int:id>/<attraction_id>", methods=["GET", "POST"])
@require_login
@require_local_admin
def admin_achievements_edit(id, attraction_id = None):
    achievement_form = AchievementForm(data_required=False, formdata=CombinedMultiDict((request.files, request.form)))
    achievement = db_session.query(Achievement).filter_by(id=id).first()

    achievement_form.attraction_id.disabled = attraction_id is None
    if attraction_id:
        achievement_form.attraction_id.data = attraction_id
        
    if not achievement or (attraction_id is not None and achievement.attraction_id != int(attraction_id)):
        flash("Achievement not found.", "error")
        return redirect(url_for("admin_achievements", page = 1, attraction_id=attraction_id)) 

    if request.method == "POST" and achievement_form.validate():
        achievement.name = achievement_form.name.data
        achievement.description = achievement_form.description.data
        achievement.pass_code = achievement_form.pass_code.data
        achievement.xp_reward = achievement_form.xp_reward.data

        achievement.attraction_id = achievement_form.attraction_id.data
        achievement.age_rating = achievement_form.age_rating.data

        db_session.commit()
        flash("Achievement updated successfully.", "success")

        return redirect(url_for("admin_achievements", page = 1, attraction_id=attraction_id))  

    achievement_form.process(obj=achievement)

    return render_template("admin_achievements_edit.html",
                           achievement=achievement_form,
                           id=id,
                           attraction_id=attraction_id,
                           title="Edit Achievement")
